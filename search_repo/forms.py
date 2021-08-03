from django import forms

BRANCH_OPTIONS = [
    ('brm_obt', 'brm_obt'),
    ('brm_sbt', 'brm_sbt'),
    ('brm_mbt', 'brm_mbt'),
]
YEAR_CHOICES = [i for i in range(2001, 2031)]

class SearchForm(forms.Form):
    title = forms.URLField(label="Enter Github Repository Link", initial='https://github.bmc.com/api/v3/repos/ZSO-STG-BRM', disabled=True)
    branch = forms.CharField(label="Select branch", widget=forms.Select(choices=BRANCH_OPTIONS))
    # username = forms.CharField(label="Enter Username")
    # password = forms.CharField(label="Enter Token")
    form_date = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES, attrs=({'style': 'width: 15%; display: inline-block;'})))
    to_date = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES, attrs=({'style': 'width: 15%; display: inline-block;'})))
