from django.urls import path, re_path

from search_repo import views

urlpatterns = [
    path('', views.search_repository.as_view(), name='search_repository'),
]