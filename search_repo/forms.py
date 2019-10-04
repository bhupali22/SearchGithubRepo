from django import forms

class SearchForm(forms.Form):
    title = forms.URLField(label="Enter Github Repository Link")
