# Generated by Django 2.2.16 on 2022-07-16 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220716_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(verbose_name='Slug'),
        ),
    ]
