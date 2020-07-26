from django.contrib import admin

from .models import Article, Digest, Recipient, Source


class DigestAdmin(admin.ModelAdmin):
    list_display = ['str_', 'sent_at']

    def str_(self, obj):
        return str(obj)

    class Meta:
        model = Digest


class SourceAdmin(admin.ModelAdmin):
    list_display = ['str_']

    def str_(self, obj):
        return str(obj)

    class Meta:
        model = Source


# Register your models here.
admin.site.register(Article)
admin.site.register(Digest, DigestAdmin)
admin.site.register(Recipient)
admin.site.register(Source, SourceAdmin)


