from django.views.generic import ListView
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
