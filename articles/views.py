from django.views.generic import ListView, TemplateView, View
from django.db.models import Q

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'

    # def get_queryset(self):
    # query = self.request.GET.get('q')
    # article_list = Article.objects.filter(
    #     title__icontains='daca').exclude(image_url='').order_by('published_at')[:11]
    # if query:
    #     article_list = Article.objects.filter(
    #         Q(title__icontains=query) |
    #         Q(description__icontains=query) |
    #         Q(author__contains=query)
    #     )
    # return article_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Define Q objects
        daca_in_title = Q(title__icontains='daca')
        empty_image_url = Q(image_url='')

        # Get featured articles first
        featured_articles = Article.objects.select_related('source').filter(
            daca_in_title & ~empty_image_url).order_by('-published_at')[:4]

        # Get recent articles, exclude ids from featured articles
        id_exclude_list = [article.id for article in featured_articles]
        recent_articles = Article.objects.select_related('source').filter(
            ~empty_image_url & ~Q(id__in=id_exclude_list)).order_by('-published_at')[:6]

        context['lead_article'] = featured_articles[0]
        context['featured_articles'] = featured_articles[1:]
        context['recent_articles'] = recent_articles
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class ArchiveView(ListView):
    model = Article
    template_name = 'articles/archive.html'
    context_object_name = 'articles'

    def get_distinct_months(self):
        return Article.objects.dates('published_at', 'month', order='DESC')

    def get_articles_by_month(self):
        pass

    def get_queryset(self):
        return Article.objects.order_by('-published_at')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add article/date grouping
        return context
