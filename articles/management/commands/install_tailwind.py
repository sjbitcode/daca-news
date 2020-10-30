import os
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite file if it already exists.',
        )

    def handle(self, *args, **options):
        tailwind_url = 'https://unpkg.com/tailwindcss@^1.0.6/dist/tailwind.min.css'
        css_dir = f'{settings.BASE_DIR}/staticfiles/css'
        tailwind_path = f'{css_dir}/tailwind.css'

        os.makedirs(css_dir, exist_ok=True)

        if os.path.exists(tailwind_path) and not options['overwrite']:
            print('The file tailwind.css already exists. Skipping.')
            return

        print('Downloading tailwind.css')
        urllib.request.urlretrieve(tailwind_url, tailwind_path)
