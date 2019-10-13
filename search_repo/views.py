from collections import defaultdict

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import requests
from .models import History, Commit, Contributor

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
                if contributors_link.status_code == 404:
                    return HttpResponse("<h1>This github url does not exist</h1>")
                elif contributors_link.status_code == 403:
                    return HttpResponse("<h1>API rate Limit exceeded</h1>")
                else:
                    response_contributors = contributors_link.json()
                    l = len(response_contributors)
                    contributors = response_contributors[l:l - 11:-1]
                    context['contributors'] = contributors
                    try:
                        new_url = History.objects.get(repo_url = repo_url_link)
                        con_obj = Contributor.objects.filter(url = new_url)
                        for _ in con_obj:
                            commit_obj = Commit.objects.get(con=_)
                            # if commit_obj.no_of_commits != contributors[_.]['total']

                            print(commit_obj.con.author_login)
                            print(commit_obj.no_of_commits)
                    except ObjectDoesNotExist:
                        new_url = History.objects.create(
                            repo_url = repo_url_link,
                        )
                        new_url.save()

                        for i in range(len(contributors)):
                            con_obj = Contributor.objects.create(
                                author_login = contributors[i]['author']['login'],
                                url = new_url,
                            )
                            con_obj.save()
                            commit_obj = Commit.objects.create(
                                no_of_commits = contributors[i]['total'],
                                con = con_obj,
                            )
                            commit_obj.save()

                    return render(request, 'search_repo/display.html',context)

        else:
            return HttpResponse("<h1>Invalid URL</h1>")