# Generated by Django 5.2.3 on 2025-06-28 16:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titolo')),
                ('content', models.TextField(verbose_name='Contenuto')),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data di Pubblicazione')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-published_date'],
            },
        ),
    ]
