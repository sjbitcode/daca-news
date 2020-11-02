from django.views.generic import ListView, TemplateView, View
from django.db.models import Count, Q

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'

    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     # article_list = Article.objects.filter(
    #     #     title__icontains='daca').exclude(image_url='').order_by('published_at')[:11]
    #     article_list = []
    #     if query:
    #         article_list = Article.objects.filter(
    #             Q(title__icontains=query) |
    #             Q(description__icontains=query) |
    #             Q(author__contains=query)
    #         )
    #         print(f'GOT SOME ARTICLES ----> {len(article_list)}')
    #     return article_list

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

        # Get top 10 news sources
        source_article_groupby = Article.objects.values(
            'source__name').annotate(Count('id')).order_by('-id__count')[:10]
        top_sources = [group['source__name'] for group in source_article_groupby]

        context['lead_article'] = featured_articles[0]
        context['featured_articles'] = featured_articles[1:]
        context['recent_articles'] = recent_articles
        context['top_sources'] = top_sources
        return context


class SearchView(ListView):
    model = Article
    template_name = 'articles/article_search.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        article_list = []
        if query:
            article_list = Article.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(author__contains=query)
            ).order_by('-published_at')
            print(f'GOT SOME ARTICLES ----> {len(article_list)}')
        return article_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queried_term'] = self.request.GET.get('q')
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
