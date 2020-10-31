from django.urls import path

from . import views


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('archive/', views.ArchiveView.as_view(), name='archive')
]
