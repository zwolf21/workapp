from django import forms



class PrnDataInputForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea)
    injgroups = forms.MultipleChoiceField(
        choices=[
            ('고가약', '고가약'), ('고위험', '고위험'), ('냉장약', '냉장약'), ('일반2', '일반2'),
            ('일반', '일반'), ('마약', '마약'), ('향정약', '향정약')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
