from django import forms


class PrnDataInputForm(forms.Form):
    prndata = forms.CharField(
        label='처방클립보드',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': '개별긴급화면에서 전체선택 체크로 전체 선택 후 복사(ctrl+c)한것을 여기에 붙이기(ctrl+v)',
            },
        )
    )
    injgroups = forms.MultipleChoiceField(
        label='주사그룹',
        choices=[
            ('고가약', '고가약'), ('고위험', '고위험'), ('냉장약', '냉장약'), ('일반2', '일반2'),
            ('일반', '일반'), ('마약', '마약'), ('향정약', '향정약')
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
    )
    bywords = forms.BooleanField(
        label='병동별로분류하기(마약향정)',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
