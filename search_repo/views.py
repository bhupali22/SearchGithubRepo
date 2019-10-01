from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView
from .forms import SearchForm

class search_repository(FormView):
    form_class = SearchForm
    template_name = 'search_repo/search.html'

