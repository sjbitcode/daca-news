from django.conf import settings


def site_url(request):
    return {'SITE_URL': settings.SITE_URL}
