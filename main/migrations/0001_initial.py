# Generated by Django 5.2.2 on 2025-06-09 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Armor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('protection_level', models.IntegerField(verbose_name='Уровень защиты')),
                ('weight', models.FloatField(verbose_name='Вес')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Броня',
                'verbose_name_plural': 'Броня',
            },
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('damage', models.IntegerField(verbose_name='Урон')),
                ('fire_rate', models.IntegerField(verbose_name='Скорострельность')),
                ('accuracy', models.IntegerField(verbose_name='Точность')),
                ('weight', models.FloatField(verbose_name='Вес')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Оружие',
                'verbose_name_plural': 'Оружие',
            },
        ),
        migrations.CreateModel(
            name='Creater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Полное имя')),
                ('bio', models.TextField(verbose_name='Биография')),
            ],
            options={
                'verbose_name': 'Создатель',
                'verbose_name_plural': 'Создатели',
            },
        ),
        migrations.CreateModel(
            name='BodyArmor',
            fields=[
                ('armor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.armor')),
                ('armor_type', models.CharField(max_length=50, verbose_name='Тип брони')),
                ('covers_torso', models.BooleanField(default=True, verbose_name='Защищает торс')),
                ('covers_groin', models.BooleanField(default=False, verbose_name='Защищает пах')),
            ],
            options={
                'verbose_name': 'Бронежилет',
                'verbose_name_plural': 'Бронежилеты',
            },
            bases=('main.armor',),
        ),
        migrations.CreateModel(
            name='Helmet',
            fields=[
                ('armor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.armor')),
                ('covers_face', models.BooleanField(default=False, verbose_name='Закрывает лицо')),
                ('has_visor', models.BooleanField(default=False, verbose_name='Имеет забрало')),
                ('material', models.CharField(max_length=50, verbose_name='Материал')),
            ],
            options={
                'verbose_name': 'Каска',
                'verbose_name_plural': 'Каски',
            },
            bases=('main.armor',),
        ),
        migrations.CreateModel(
            name='LimbProtection',
            fields=[
                ('armor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.armor')),
                ('protects_arms', models.BooleanField(default=False, verbose_name='Защищает руки')),
                ('protects_legs', models.BooleanField(default=False, verbose_name='Защищает ноги')),
                ('is_flexible', models.BooleanField(default=True, verbose_name='Гибкий материал')),
            ],
            options={
                'verbose_name': 'Защита конечностей',
                'verbose_name_plural': 'Защита конечностей',
            },
            bases=('main.armor',),
        ),
        migrations.CreateModel(
            name='AssaultRifle',
            fields=[
                ('weapon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.weapon')),
                ('magazine_size', models.IntegerField(verbose_name='Размер магазина')),
                ('caliber', models.CharField(max_length=20, verbose_name='Калибр')),
                ('has_auto_mode', models.BooleanField(default=True, verbose_name='Автоматический режим')),
            ],
            options={
                'verbose_name': 'Автомат',
                'verbose_name_plural': 'Автоматы',
            },
            bases=('main.weapon',),
        ),
        migrations.CreateModel(
            name='MachineGun',
            fields=[
                ('weapon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.weapon')),
                ('belt_fed', models.BooleanField(default=True, verbose_name='Ленточное питание')),
                ('bipod_included', models.BooleanField(default=True, verbose_name='Сошки в комплекте')),
                ('cooling_system', models.CharField(max_length=50, verbose_name='Система охлаждения')),
            ],
            options={
                'verbose_name': 'Пулемёт',
                'verbose_name_plural': 'Пулемёты',
            },
            bases=('main.weapon',),
        ),
        migrations.CreateModel(
            name='MeleeWeapon',
            fields=[
                ('weapon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.weapon')),
                ('blade_length', models.FloatField(verbose_name='Длина клинка')),
                ('material', models.CharField(max_length=50, verbose_name='Материал')),
                ('is_double_edged', models.BooleanField(default=False, verbose_name='Двусторонняя заточка')),
            ],
            options={
                'verbose_name': 'Холодное оружие',
                'verbose_name_plural': 'Холодное оружие',
            },
            bases=('main.weapon',),
        ),
        migrations.CreateModel(
            name='Pistol',
            fields=[
                ('weapon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.weapon')),
                ('caliber', models.CharField(max_length=20, verbose_name='Калибр')),
                ('magazine_size', models.IntegerField(verbose_name='Размер магазина')),
                ('is_semi_auto', models.BooleanField(default=True, verbose_name='Полуавтоматический')),
            ],
            options={
                'verbose_name': 'Пистолет',
                'verbose_name_plural': 'Пистолеты',
            },
            bases=('main.weapon',),
        ),
        migrations.CreateModel(
            name='Shotgun',
            fields=[
                ('weapon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.weapon')),
                ('gauge', models.IntegerField(verbose_name='Калибр')),
                ('pump_action', models.BooleanField(default=False, verbose_name='Помповый механизм')),
                ('shell_capacity', models.IntegerField(verbose_name='Ёмкость магазина')),
            ],
            options={
                'verbose_name': 'Дробовик',
                'verbose_name_plural': 'Дробовики',
            },
            bases=('main.weapon',),
        ),
        migrations.CreateModel(
            name='SniperRifle',
            fields=[
                ('weapon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.weapon')),
                ('zoom_level', models.IntegerField(verbose_name='Уровень увеличения')),
                ('bolt_action', models.BooleanField(default=False, verbose_name='Скользящий затвор')),
                ('caliber', models.CharField(max_length=20, verbose_name='Калибр')),
            ],
            options={
                'verbose_name': 'Снайперская винтовка',
                'verbose_name_plural': 'Снайперские винтовки',
            },
            bases=('main.weapon',),
        ),
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('type', models.CharField(max_length=50, verbose_name='Тип аксессуара')),
                ('weight', models.FloatField(verbose_name='Вес')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('compatible_with', models.ManyToManyField(blank=True, to='main.weapon', verbose_name='Совместимо с')),
            ],
            options={
                'verbose_name': 'Аксессуар',
                'verbose_name_plural': 'Акссуары',
            },
        ),
    ]
