from django.db import models
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit

class Creater(models.Model):
    name = models.CharField("Полное имя", max_length=80)
    bio = models.TextField("Биография")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def parse_object(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class BaseItem(models.Model):
    name = models.CharField("Название", max_length=120)
    description = models.TextField("Описание")
    weight = models.FloatField("Вес")
    price = models.FloatField("Цена")
    date_added = models.DateTimeField("Дата добавления", auto_now_add=True)
    cover = models.ImageField("Обложка", upload_to="covers/", null=True, blank=True)
    cover_card = ImageSpecField([ResizeToFit(200, 200)], source="cover", format="PNG")
    creator = models.ForeignKey(Creater, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Производитель")

    class Meta:
        abstract = True

    @property
    def category(self):
        if isinstance(self, Weapon):
            if isinstance(self, AssaultRifle):
                return 'assault'
            elif isinstance(self, SniperRifle):
                return 'sniper'
            elif isinstance(self, MachineGun):
                return 'assault'  # Пистолеты-пулеметы
            elif isinstance(self, Shotgun):
                return 'shotgun'
            elif isinstance(self, MeleeWeapon):
                return 'melee'
            elif isinstance(self, Pistol):
                return 'pistol'
            return 'weapon'
        elif isinstance(self, Armor):
            return 'armor'
        elif isinstance(self, Accessory):
            return 'accessory'
        return 'other'

    def __str__(self):
        return self.name

# Модели для оружия и подклассов
class Weapon(BaseItem):
    damage = models.IntegerField("Урон")
    fire_rate = models.IntegerField("Скорострельность")
    accuracy = models.IntegerField("Точность")

    class Meta:
        verbose_name = "Оружие"
        verbose_name_plural = "Оружие"

class AssaultRifle(Weapon):
    magazine_size = models.IntegerField("Размер магазина")
    caliber = models.CharField("Калибр", max_length=20)
    has_auto_mode = models.BooleanField("Автоматический режим", default=True)

    class Meta:
        verbose_name = "Автомат"
        verbose_name_plural = "Автоматы"

class SniperRifle(Weapon):
    zoom_level = models.IntegerField("Уровень увеличения")
    bolt_action = models.BooleanField("Скользящий затвор", default=False)
    caliber = models.CharField("Калибр", max_length=20)

    class Meta:
        verbose_name = "Снайперская винтовка"
        verbose_name_plural = "Снайперские винтовки"

class MachineGun(Weapon):
    belt_fed = models.BooleanField("Ленточное питание", default=True)
    bipod_included = models.BooleanField("Сошки в комплекте", default=True)
    cooling_system = models.CharField("Система охлаждения", max_length=50)

    class Meta:
        verbose_name = "Пулемёт"
        verbose_name_plural = "Пулемёты"

class Shotgun(Weapon):
    gauge = models.IntegerField("Калибр")
    pump_action = models.BooleanField("Помповый механизм", default=False)
    shell_capacity = models.IntegerField("Ёмкость магазина")

    class Meta:
        verbose_name = "Дробовик"
        verbose_name_plural = "Дробовики"

class MeleeWeapon(Weapon):
    blade_length = models.FloatField("Длина клинка")
    material = models.CharField("Материал", max_length=50)
    is_double_edged = models.BooleanField("Двусторонняя заточка", default=False)

    class Meta:
        verbose_name = "Холодное оружие"
        verbose_name_plural = "Холодное оружие"

class Pistol(Weapon):
    caliber = models.CharField("Калибр", max_length=20)
    magazine_size = models.IntegerField("Размер магазина")
    is_semi_auto = models.BooleanField("Полуавтоматический", default=True)

    class Meta:
        verbose_name = "Пистолет"
        verbose_name_plural = "Пистолеты"

# Модели для брони и подклассов
class Armor(BaseItem):
    protection_level = models.IntegerField("Уровень защиты")

    class Meta:
        verbose_name = "Броня"
        verbose_name_plural = "Броня"

class Helmet(Armor):
    covers_face = models.BooleanField("Закрывает лицо", default=False)
    has_visor = models.BooleanField("Имеет забрало", default=False)
    material = models.CharField("Материал", max_length=50)

    class Meta:
        verbose_name = "Каска"
        verbose_name_plural = "Каски"

class BodyArmor(Armor):
    armor_type = models.CharField("Тип брони", max_length=50)
    covers_torso = models.BooleanField("Защищает торс", default=True)
    covers_groin = models.BooleanField("Защищает пах", default=False)

    class Meta:
        verbose_name = "Бронежилет"
        verbose_name_plural = "Бронежилеты"

class LimbProtection(Armor):
    protects_arms = models.BooleanField("Защищает руки", default=False)
    protects_legs = models.BooleanField("Защищает ноги", default=False)
    is_flexible = models.BooleanField("Гибкий материал", default=True)

    class Meta:
        verbose_name = "Защита конечностей"
        verbose_name_plural = "Защита конечностей"

# Модель для аксессуаров
class Accessory(BaseItem):
    type = models.CharField("Тип аксессуара", max_length=50)
    compatible_with = models.ManyToManyField(Weapon, blank=True, verbose_name="Совместимо с")

    class Meta:
        verbose_name = "Аксессуар"
        verbose_name_plural = "Аксессуары"