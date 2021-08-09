import re, math
import pandas as pd
import numpy as np
import io
from datetime import datetime

from pandas.core import groupby



def _load_drug_df(f, ini_header_name='약품코드', _find_header_retry=5, _header=0):
    if _find_header_retry ==0:
        raise ValueError("{} 을 포함하는 컬럼을 찾을수 없습니다.".format(ini_header_name))
    df = pd.read_excel(f, header=_header, keep_default_na=False)
    if ini_header_name not in df.columns:
        df = _load_drug_df(
            f, ini_header_name=ini_header_name, _find_header_retry=_find_header_retry-1, _header=_header+1
        )
    
    df = df.rename(lambda n: re.sub("\s+|_x000D_", '', n), axis='columns')
    return df



PRN_COLUMNS = [
    '발행처', '등록번호', '환자명', 'No.', '약품코드', '약품명', '투여량', '횟수', '일수', '총량', '용법', 'ADC', 'PRN', '퇴원', '처방의사', '입력일시',
    '투약번호', '차수', '접수일시'
]
def _load_prn_df(f, sep='	',names=PRN_COLUMNS):
    f = io.StringIO(f)
    return pd.read_csv(f, sep=sep, names=names)



def create_prn(eumc_drug_obj, prndata, injgroups, bywords=False):
    df_drug = _load_drug_df(eumc_drug_obj.rawdata.file)
    df_prn = _load_prn_df(prndata)
    df_prn = pd.merge(df_prn, df_drug, left_on=['약품명'], right_on=['상용약품명'])
    df_prn = df_prn[['발행처', '약품명', '기본투여단위', '함량', '환산단위', '투여량', '주사그룹번호(입)', '입력일시']]
    df_prn[['투여량_amt', '투여량_unit']] = df_prn['투여량'].str.extract(r'(\d*\.?\d)\s*(\w+)')
    df_prn[['함량_amt', '함량_unit']] = df_prn['함량'].str.extract(r'(\d*\.?\d)\s*(\w+)')
    df_prn = df_prn.astype({'투여량_amt': np.float64, '함량_amt': np.float64})
    df_prn['수량'] = np.where(df_prn['환산단위']==df_prn['투여량_unit'], df_prn['투여량_amt'], df_prn['투여량_amt']/df_prn['함량_amt'])
    df_prn['수량'] = np.ceil(df_prn['수량'])
    
    ordered_last = df_prn['입력일시'].max() # 최종 오더시간 구하기
    injgroups = injgroups or ['고가', '고위험', '냉장약', '일반2']
    exp_mask = df_prn['주사그룹번호(입)'].isin(injgroups)
    df_ret = df_prn[exp_mask]

    if bywords is True:
        df_pvt = pd.pivot_table(df_ret, values=['수량'], index=['주사그룹번호(입)', '약품명', '발행처'], aggfunc='sum')
        df_pvt = df_pvt.astype({'수량': np.int64})
        pvt_html = df_pvt.to_html(classes='table table-sm table-bordered', justify='center')

    df_ret = df_ret.groupby(['약품명', '환산단위', '주사그룹번호(입)'], group_keys=False).agg('sum')[['수량']].reset_index()
    df_ret = df_ret[['주사그룹번호(입)', '약품명', '수량', '환산단위']]
    df_ret = df_ret.sort_values(['주사그룹번호(입)', '약품명'])        
    df_ret = df_ret.astype({'수량': np.int64})

    count_at = datetime.now().strftime("%Y-%m-%d %H:%M:%s")
    table_html = df_ret.to_html(classes='table table-sm table-bordered', justify='center', index=False)
    table_html+= f"<p>집계일시: {count_at}</p>"
    if bywords is True:
        table_html+=pvt_html
    return table_html


