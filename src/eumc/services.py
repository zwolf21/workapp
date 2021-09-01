import re, io

import pandas as pd
import numpy as np
from datetime import datetime


PRN_COLUMNS = [
    '발행처', '등록번호', '환자명', 'No.', '약품코드', '약품명', '투여량', '횟수', '일수', '총량', '용법', 'ADC', 'PRN', '퇴원', '처방의사', '입력일시',
    '투약번호', '차수', '접수일시'
]


def _load_drug_df(f, ini_header_name='약품코드', _find_header_retry=5, _header=0):
    if _find_header_retry == 0:
        raise ValueError("{} 을 포함하는 컬럼을 찾을수 없습니다.".format(ini_header_name))
    df = pd.read_excel(f, header=_header, keep_default_na=False)
    if ini_header_name not in df.columns:
        df = _load_drug_df(
            f, ini_header_name=ini_header_name, _find_header_retry=_find_header_retry-1, _header=_header+1
        )

    df = df.rename(lambda n: re.sub("\s+|_x000D_", '', n), axis='columns')
    return df


def _load_prn_df(f, sep='	', names=PRN_COLUMNS):
    f = io.StringIO(f)
    return pd.read_csv(f, sep=sep, names=names)


def _split_amtunit(df, columns, pfix_amt='amt', pfix_unit='unit', amt_astype=np.float64):
    if isinstance(columns, str):
        columns = [columns]
    for column in columns:
        column_amt = f"{column}_{pfix_amt}"
        column_unit = f"{column}_{pfix_unit}"
        df[[column_amt, column_unit]] = df[column].str.extract(r"(\d*\.?\d+)\s*(\w+)")
        df = df.astype({column_amt: amt_astype})
    return df


def create_prn(eumc_drug_obj, prndata, injgroups, bywords=False):
    df_drug = _load_drug_df(eumc_drug_obj.rawdata.file)
    df_prn = _load_prn_df(prndata)
    df_prn = pd.merge(df_prn, df_drug, left_on=['약품명'], right_on=['상용약품명'])
    df_prn = df_prn[['발행처', '약품명', '기본투여단위', '함량', '규격', '환산단위', '투여량', '주사그룹번호(입)', '입력일시']]


    # '15 ml' -> [15, 'ml'] '0.075 mg' -> [0.075, 'mg']: X_amt, X_unit
    df_prn = _split_amtunit(df_prn, ['투여량', '함량', '규격'])

    #1. 처방을 환산단위로 바로 낸 경우 투여량을 그냥 적용
    mask1 = df_prn['환산단위'] == df_prn['투여량_unit']
    df_prn.loc[mask1, '수량'] = df_prn['투여량_amt']
    
    # 2. 처방을 함량(mg)으로 낸 경우 투여량을 함량으로 나눠줌, 위의 1 처리를 한 그룹과 겹치지 않기위해 ~mask
    mask2 = df_prn['함량_unit'] == df_prn['투여량_unit']; mask2 = (~mask1 & mask2)
    df_prn.loc[mask2, '수량'] = df_prn['투여량_amt'] / df_prn['함량_amt']

    #3. 처방을 규격(ml)으로 낸 경우, 투여량을 규격량으로 나눠줌, 위의 1,2 처리를 한 그룹과 겹치지 않기 위한 ~(mask1|mask2)
    mask3 = df_prn['규격_unit'] == df_prn['투여량_unit']; mask3 = (~(mask1 | mask2) & mask3)
    df_prn.loc[mask3, '수량'] = df_prn['투여량_amt'] / df_prn['규격_amt']


    df_prn['수량'] = np.ceil(df_prn['수량'])

    ordered_last = df_prn['입력일시'].max()  # 최종 오더시간 구하기
    injgroups = injgroups or ['고가약', '고위험', '냉장약', '일반2']
    exp_mask = df_prn['주사그룹번호(입)'].isin(injgroups)
    df_ret = df_prn[exp_mask]

    if bywords is True:
        def pivot(df):
            pvt = pd.pivot_table(df, values=['수량'], index=['발행처'], aggfunc='sum', margins=True, margins_name='합계')
            pvt = pvt.astype({'수량': np.int64})
            return pvt

        df_pvt = df_ret.groupby(['주사그룹번호(입)', '약품명']).apply(pivot)
        html = df_pvt.to_html(classes='table table-sm table-bordered', justify='center')
    else:
        df_ret = df_ret.groupby(['약품명', '환산단위', '주사그룹번호(입)'], group_keys=False).agg('sum')[['수량']].reset_index()
        df_ret = df_ret[['주사그룹번호(입)', '약품명', '수량', '환산단위']]
        df_ret = df_ret.sort_values(['주사그룹번호(입)', '약품명'])
        df_ret = df_ret.astype({'수량': np.int64})
        html = df_ret.to_html(classes='table table-sm table-bordered', justify='center', index=False)

    count_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html += f"<p>집계일시: {count_at}</p>"
    return html