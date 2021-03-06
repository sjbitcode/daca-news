import html

from django import forms
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags

from .models import ApiResponse, Article, Source


def strip_tags_and_format(html_str):
    html_str = html.unescape(html_str)
    return strip_tags(html_str)


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        return strip_tags_and_format(name.lower())

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']
        slug = cleaned_data['slug']

        if not slug:
            cleaned_data['slug'] = slugify(name)

        return cleaned_data


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at']

    def clean_title(self):
        title = self.cleaned_data['title']
        return strip_tags_and_format(title)

    def clean_author(self):
        author = self.cleaned_data['author']
        return strip_tags_and_format(author)

    def clean_description(self):
        description = self.cleaned_data['description']
        return strip_tags_and_format(description)

    def clean_image_url(self):
        image_url = self.cleaned_data['image_url']
        # For Bing images
        return image_url.replace('pid=News', 'pid=')


class ApiResponseForm(forms.ModelForm):
    class Meta:
        model = ApiResponse
        exclude = ['created_at']
