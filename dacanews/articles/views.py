from django.views.generic import ListView, View
from django.db.models import Q

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        query = self.request.GET.get('q')
        article_list = Article.objects.order_by('published_at')[:10]
        if query:
            article_list = Article.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(author__contains=query)
            )
        return article_list


class ArchiveView(ListView):
    model = Article
    template_name = 'articles/archive.html'
    context_object_name = 'articles'

    def get_distinct_months(self):
        return Article.objects.dates('published_at', 'month', order='DESC')

    def get_articles_by_month(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add article/date grouping
        return context
