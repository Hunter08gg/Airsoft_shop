# Generated by Django 5.2.2 on 2025-06-11 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='armor',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name='Обложка'),
        ),
        migrations.AddField(
            model_name='weapon',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name='Обложка'),
        ),
    ]
