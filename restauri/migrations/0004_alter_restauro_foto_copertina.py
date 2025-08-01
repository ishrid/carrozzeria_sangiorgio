# Generated by Django 5.2.3 on 2025-07-06 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restauri', '0003_restauro_foto_copertina'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restauro',
            name='foto_copertina',
            field=models.ImageField(help_text='Immagine specifica da usare come copertina.', upload_to='restauri_copertine/', verbose_name='Immagine di Copertina dedicata'),
        ),
    ]
