from django.shortcuts import render
import requests

# Create your views here.
from django.views.generic import FormView
from .forms import SearchForm

class search_repository(FormView):
    form_class = SearchForm
    template_name = 'search_repo/search.html'

    def form_valid(self, form):
        url_link = form.cleaned_data.get('title')
        response = requests.get(url_link)
        print(response)
