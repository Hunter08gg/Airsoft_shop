# Generated by Django 5.2.2 on 2025-06-11 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_armor_cover_weapon_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessory',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name='Обложка'),
        ),
    ]
