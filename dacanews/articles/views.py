from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Article


def index(request):
    articles = Article.objects.order_by('published_at')[:10]
    context = {'articles': articles, }
    return render(request, 'articles/index.html', context)
