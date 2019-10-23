from django.db import models
# https://stackoverflow.com/questions/32988532/django-models-best-way-to-save-multiple-values

# Create your models here.
<<<<<<< HEAD


=======
class History(models.Model):
    repo_url = models.URLField(max_length=700)

    def __str__(self):
        return "%s" %(self.repo_url)

    def update_data(self, contributors):
        con_obj = Contributor.objects.filter(url = self)
        i = 0
        for _ in con_obj:
            commit_obj = Commit.objects.get(contributor=_)
            i = i + 1
            if _.ranking == i:
                if commit_obj.contributor.author_login == contributors[i - 1]['author']['login']:
                    if commit_obj.no_of_commits == contributors[i - 1]['total']:
                        pass
                    else:
                        commit_obj.no_of_commits = contributors[i - 1]['total']
                        commit_obj.save()
                else:
                    _.delete()
                    self.add_data(i=i-1,contributors=contributors)
        while (i != len(contributors)):
            self.add_data(i, contributors)
            i = i+1

    def save_new_data(self, contributors):
        for i in range(len(contributors)):
            self.add_data(i, contributors)


    def add_data(self, i, contributors):
        con_obj = Contributor.objects.create(
            author_login=contributors[i]['author']['login'],
            url=self,
            ranking=i + 1,
        )
        con_obj.save()
        commit_obj = Commit.objects.create(
            no_of_commits=contributors[i]['total'],
            contributor=con_obj,
        )
        commit_obj.save()


class Contributor(models.Model):
    author_login = models.CharField(max_length=500)
    url = models.ForeignKey(History, on_delete=models.CASCADE)
    ranking = models.IntegerField()

    def __str__(self):
        return "%s" %(self.author_login)


class Commit(models.Model):
    no_of_commits = models.IntegerField(default=0)
    contributor = models.OneToOneField(Contributor, on_delete=models.CASCADE)
>>>>>>> model_branch
