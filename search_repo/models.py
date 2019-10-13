from django.db import models
# https://stackoverflow.com/questions/32988532/django-models-best-way-to-save-multiple-values

# Create your models here.
class History(models.Model):
    repo_url = models.URLField(max_length=700)

    def __str__(self):
        return "%s" %(self.repo_url)


class Contributor(models.Model):
    author_login = models.CharField(max_length=500)
    url = models.ForeignKey(History, on_delete=models.CASCADE)
    ranking = models.IntegerField()

    def __str__(self):
        return "%s" %(self.author_login)


class Commit(models.Model):
    no_of_commits = models.IntegerField(default=0)
    con = models.OneToOneField(Contributor, on_delete=models.CASCADE)

