import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from .forms import SearchForm

class search_repository(FormView):
    form_class = SearchForm
    template_name = 'search_repo/search.html'
    success_url = reverse_lazy('DisplayView')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data(**kwargs)

        if form.is_valid():
            url_link = form.cleaned_data.get('title')
            print("In form valid", url_link)

            base_url = "https://api.github.com/repos/"

            new_url_link = url_link.strip().replace("https://github.com/", '')
            print(new_url_link)

            user_name = list(map(str, new_url_link.split('/')))
            print(user_name)

            repo_link = base_url + user_name[0] + '/' + user_name[1] + '/contributors?per_page=10'
            print(repo_link)
            contributors_link = requests.get(repo_link)

            response_contributors = contributors_link.json()

            # print(response_contributors)

            # distros_dict = json.loads(response_contributors)

            context['contributors'] = response_contributors

            return render(request, 'search_repo/display.html',context)
            # return self.render_to_response(context)

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())


class DisplayView(TemplateView):
    template_name = 'search_repo/display.html'

