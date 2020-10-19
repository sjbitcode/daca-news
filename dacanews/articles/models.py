from django.db import models


# Create your models here.
class Article(models.Model):
    source = models.ForeignKey('Source', on_delete=models.CASCADE, max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(unique=True)
    image_url = models.URLField(blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f'Article [title - {self.title[:20]}, source - {self.source_id}]'


class Source(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f'Source {self.slug} {self.id}'


class ApiResponse(models.Model):
    source = models.CharField(max_length=20, blank=True)
    response = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return f'APIResponse [source - {self.source}, created - {self.created_at}]'


class Digest(models.Model):
    sent_at = models.DateTimeField(auto_now_add=True)
    articles = models.ManyToManyField('Article')
    recipients = models.ManyToManyField('Recipient')

    def __str__(self):
        return f'Digest {self.id}'


class Recipient(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'Recipient [email - {self.email}, name - {self.name}]'
