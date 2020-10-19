import html

from django import forms
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags

from .models import ApiResponse, Article, Source


# class MLStripper(html.parser.HTMLParser):
#     def __init__(self):
#         super().__init__()
#         self.reset()
#         self.strict = False
#         self.convert_charrefs = True
#         self.text = io.StringIO()

#     def handle_data(self, d):
#         self.text.write(d)

#     def get_data(self):
#         return self.text.getvalue()


def strip_tags_and_format(html_str):
    html_str = html.unescape(html_str)
    return strip_tags(html_str)
    # s = MLStripper()
    # s.feed(html_str)
    # return s.get_data()


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = '__all__'

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


class ApiResponseForm(forms.ModelForm):
    class Meta:
        model = ApiResponse
        exclude = ['created_at']
