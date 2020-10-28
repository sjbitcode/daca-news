from django.urls import path

from . import views


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='index'),
    path('archive/', views.ArchiveView.as_view(), name='archive')
]
