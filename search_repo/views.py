import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import requests

# Create your views here.
from django.views.generic import FormView, TemplateView
from .forms import SearchForm

class search_repository(FormView):
    form_class = SearchForm
    template_name = 'search_repo/search.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data(**kwargs)

        if form.is_valid():
            url_link = form.cleaned_data.get('title')
            base_url = "https://api.github.com/repos/"

            try:
                new_url_link = url_link.strip().replace("https://github.com/", '')
                user_name = list(map(str, new_url_link.split('/')))
                repo_link = base_url + user_name[0] + '/' + user_name[1] + '/stats/contributors'
            except:
                return HttpResponse("<h1>No such repository found</h1>")
            else:
                contributors_link = requests.get(repo_link)
                response_contributors = contributors_link.json()
                try:
                    if response_contributors['message'] == "Not Found":
                        return HttpResponse("<h1>This github url does not exist</h1>")
                except:
                    l = len(response_contributors)
                    contributors = response_contributors[l:l - 11:-1]
                    context['contributors'] = contributors
                    return render(request, 'search_repo/display.html',context)

        else:
            return HttpResponse("<h1>Invalid URL</h1>")




