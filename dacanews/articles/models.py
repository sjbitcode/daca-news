from django.db import models

# Create your models here.
class Article(models.Model):
    source = models.ForeignKey('Source', on_delete=models.CASCADE, max_length=100)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(unique=True)
    image_url = models.URLField(blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Article [title - {self.title[:20]}, source - {self.source_id}]'


class Source(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name_slug


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
