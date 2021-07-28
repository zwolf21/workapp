from django import forms


class PrnDataInputForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea)
