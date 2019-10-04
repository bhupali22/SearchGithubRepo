from collections import defaultdict
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
        users_dict = defaultdict(list)

        if form.is_valid():
            url_link = form.cleaned_data.get('title')
            base_url = "https://api.github.com/"

            try:
                new_url_link = url_link.strip().replace("https://github.com/", '')
                user_name = list(map(str, new_url_link.split('/')))
                repo_link = base_url + 'repos/' + user_name[0] + '/' + user_name[1] + '/stats/contributors'
            except:
                return HttpResponse("<h1>No such repository found</h1>")
            else:
                contributors_link = requests.get(repo_link)
                if contributors_link.status_code == 404:
                    return HttpResponse("<h1>This github url does not exist</h1>")
                elif contributors_link.status_code == 403:
                    return HttpResponse("<h1>API rate Limit exceeded</h1>")
                else:
                    response_contributors = contributors_link.json()
                    l = len(response_contributors)
                    contributors = response_contributors[l:l - 11:-1]
                    context['contributors'] = contributors
                    return render(request, 'search_repo/display.html',context)

        else:
            return HttpResponse("<h1>Invalid URL</h1>")




