# Generated by Django 3.0.8 on 2020-07-26 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20200720_1643'),
    ]

    operations = [
        migrations.RenameField(
            model_name='source',
            old_name='name_slug',
            new_name='slug',
        ),
    ]
