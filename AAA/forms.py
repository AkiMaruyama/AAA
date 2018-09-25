from django import forms

class LinkForm(forms.Form):
    link = forms.CharField(label='link', max_length=100)
    