# Generated by Django 3.0.8 on 2020-07-19 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_digest_recipient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]