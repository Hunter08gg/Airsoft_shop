# Generated by Django 5.2.2 on 2025-06-11 17:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_accessory_cover'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accessory',
            options={'verbose_name': 'Аксессуар', 'verbose_name_plural': 'Аксессуары'},
        ),
        migrations.AddField(
            model_name='accessory',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.creater', verbose_name='Производитель'),
        ),
        migrations.AddField(
            model_name='armor',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.creater', verbose_name='Производитель'),
        ),
        migrations.AddField(
            model_name='weapon',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.creater', verbose_name='Производитель'),
        ),
    ]
