# Generated by Django 5.2.3 on 2025-07-10 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendita', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='veicoloinvendita',
            name='status',
            field=models.CharField(choices=[('disponibile', 'Disponibile'), ('trattativa', 'In Trattativa'), ('venduto', 'Venduto')], default='disponibile', max_length=20),
        ),
    ]
