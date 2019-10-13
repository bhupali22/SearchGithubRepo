from django.contrib import admin
from .models import History, Contributor, Commit
# Register your models here.


class HistoryAdmin(admin.ModelAdmin):
    list_display = ("repo_url",)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("author_login",)


class CommitAdmin(admin.ModelAdmin):
    list_display = ("no_of_commits",)


admin.site.register(History, HistoryAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Commit, CommitAdmin)