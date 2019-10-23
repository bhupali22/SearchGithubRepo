from collections import defaultdict
<<<<<<< HEAD
=======
import time
from django.core.exceptions import ObjectDoesNotExist
>>>>>>> model_branch
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import requests
from .models import History, Commit, Contributor

# Create your views here.
<<<<<<< HEAD
from django.views.generic import FormView, TemplateView
=======
from django.views.generic import FormView, TemplateView, ListView
>>>>>>> model_branch
from .forms import SearchForm

class search_repository(FormView):
    form_class = SearchForm
    template_name = 'search_repo/search.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data(**kwargs)
<<<<<<< HEAD
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




=======
        if "api_fetch" in request.POST:
            if form.is_valid():
                repo_url_link = form.cleaned_data.get('title')
                url_link = repo_url_link
                base_url = "https://api.github.com/"

                try:
                    new_url_link = url_link.strip().replace("https://github.com/", '')
                    user_name = list(map(str, new_url_link.split('/')))
                    repo_link = base_url + 'repos/' + user_name[0] + '/' + user_name[1] + '/stats/contributors'
                except:
                    return HttpResponse("<h1>No such repository found</h1>")
                else:
                    contributors_link = requests.get(repo_link)
                    while(contributors_link.status_code == 202):
                        print(contributors_link)
                        time.sleep(2)
                        contributors_link = requests.get(repo_link)
                    if contributors_link.status_code == 404:
                        return HttpResponse("<h1>This github url does not exist</h1>")
                    elif contributors_link.status_code == 403:
                        return HttpResponse("<h1>API rate Limit exceeded</h1>")
                    else:
                        response_contributors = list(contributors_link.json())
                        response_contributors.reverse()
                        contributors = response_contributors[0:10]
                        context['contributors'] = contributors
                        try:
                            new_url = History.objects.get(repo_url=repo_url_link)
                            new_url.update_data(contributors)
                        except ObjectDoesNotExist:
                            new_url = History.objects.create(
                                repo_url=repo_url_link,
                            )
                            new_url.save()
                            new_url.save_new_data(contributors)
                        return render(request, 'search_repo/display.html', context)

            else:
                return HttpResponse("<h1>Invalid URL</h1>")

        if "database_fetch" in request.POST:
            if form.is_valid():
                repo_url_link = form.cleaned_data.get('title')
                try:
                    query_set = History.objects.get(repo_url = repo_url_link)
                except ObjectDoesNotExist:
                    return HttpResponse("<h1>No history available for this url</h1>")
                dict1 = defaultdict()
                contributors_set = Contributor.objects.filter(url=query_set.id).order_by('ranking')
                for contrib in contributors_set:
                    result = Commit.objects.get(contributor = contrib)
                    dict1[contrib] = result.no_of_commits
                context['contributors_set'] = dict1

                return render(request, 'search_repo/display_from_database.html',context)
>>>>>>> model_branch
