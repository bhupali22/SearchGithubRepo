from collections import defaultdict
import time, csv
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import requests
from .models import History, Commit, Contributor
from datetime import datetime
import pandas as pd

# Create your views here.
from django.views.generic import FormView, TemplateView, ListView
from .forms import SearchForm

class search_repository(FormView):
    form_class = SearchForm
    template_name = 'search_repo/search.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data(**kwargs)
        csv_data = []
        page = 1
        flag = True

        if "api_fetch" in request.POST:
            if form.is_valid():
                repo_url_link = form.cleaned_data.get('title')
                branch_name = form.cleaned_data.get('branch')
                from_date = form.cleaned_data.get('form_date')
                to_date = form.cleaned_data.get('to_date')

                if from_date > to_date:
                    return HttpResponse("<h1>Wrong from date and to date selected</h1>")

                while(flag) :
                    try:
                        new_url_link = repo_url_link + '/' + branch_name + '/pulls?access_token=ffb2ce7632c3ff6b0d5c18fa1fc4ce933434bc06&state=all&page={}'.format(page)
                        print(new_url_link)
                        # new_url_link = 'https://api.github.com/repos/apple/swift-algorithms/pulls?state=all&page={}'.format(page)
                    except:
                        return HttpResponse("<h1>No such repository found</h1>")
                    else:
                        response_data = self.get_data(new_url_link)
                        if type(response_data) == HttpResponse:
                            return response_data
                        for response in response_data:
                            if response['created_at'].split('T')[0] <= str(to_date):
                                if str(from_date) <= response['created_at'].split('T')[0]:
                                    com_obj = {
                                        'changelist_no': response['number'],
                                        'summary': response['title'],
                                        'author': response['user']['login'],
                                        'comments_url': response['review_comments_url'] + "?access_token=ffb2ce7632c3ff6b0d5c18fa1fc4ce933434bc06",
                                        # 'comments_url': response['review_comments_url'],
                                        'review_comments': []
                                    }
                                    csv_data.append(com_obj)
                                if str(from_date) > response['created_at'].split('T')[0]:
                                    flag = False
                                    break
                        else:
                            page += 1
                            flag = True

                output_file = open("output.csv", "w")
                dict_writer = csv.DictWriter(output_file, ['changelist_no', 'summary', 'author', 'comment', 'reviewer'])
                dict_writer.writeheader()

                for com_obj in csv_data:
                    all_review_comments = self.get_data(com_obj['comments_url'])

                    if type(all_review_comments) == HttpResponse:
                        return all_review_comments

                    for com in all_review_comments:
                        comment_obj = {
                            'comment': com['body'],
                            'reviewer': com['user']['login']
                        }
                        com_obj['review_comments'].append(comment_obj)
                    com_obj.pop('comments_url')

                dict_writer.writerows(csv_data)
                context['header'] = "Data Dump to output.csv"
                output_file.close()

                return render(request, 'search_repo/display.html', context)

            else:
                return HttpResponse("<h1>Invalid URL</h1>")

    def get_data(self, url_link):
        data = requests.get(url_link)
        while (data.status_code == 202):
            print(contributors_link)
            time.sleep(2)
            data = requests.get(url_link)
        if data.status_code == 404:
            return HttpResponse("<h1>This github url does not exist</h1>")
        elif data.status_code == 403:
            return HttpResponse("<h1>API rate Limit exceeded</h1>")
        else:
            return list(data.json())