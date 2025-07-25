# Generated by Django 5.2.3 on 2025-07-04 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_fotoofficina'),
    ]

    operations = [
        migrations.AddField(
            model_name='fotoofficina',
            name='max_width',
            field=models.PositiveIntegerField(blank=True, default=416, help_text='Opzionale: imposta una larghezza massima in pixel per questa immagine nella galleria. Utile per immagini panoramiche o più larghe.', null=True),
        ),
    ]
