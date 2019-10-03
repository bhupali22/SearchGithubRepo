from django.urls import path

from search_repo import views

urlpatterns = [
    path('', views.search_repository.as_view(), name='search_repository'),
    path('display/', views.DisplayView.as_view(), name='DisplayView')
]