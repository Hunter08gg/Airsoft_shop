from django.contrib import admin
from main.models import (
    Creater,
    Weapon, AssaultRifle, SniperRifle, MachineGun, Shotgun, MeleeWeapon, Pistol,
    Armor, Helmet, BodyArmor, LimbProtection,
    Accessory
)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профили'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ('name', 'damage', 'fire_rate', 'price', 'creator')
    list_filter = ('creator',)
    search_fields = ('name', 'description')

class ArmorAdmin(admin.ModelAdmin):
    list_display = ('name', 'protection_level', 'weight', 'price', 'creator')
    list_filter = ('creator',)
    search_fields = ('name', 'description')

class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'weight', 'price', 'creator')
    list_filter = ('creator', 'type')
    search_fields = ('name', 'description')
    filter_horizontal = ('compatible_with',)

class CreaterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'bio')

# Регистрация базовых классов
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Creater, CreaterAdmin)

# Регистрация подклассов оружия
admin.site.register(AssaultRifle, WeaponAdmin)
admin.site.register(SniperRifle, WeaponAdmin)
admin.site.register(MachineGun, WeaponAdmin)
admin.site.register(Shotgun, WeaponAdmin)
admin.site.register(MeleeWeapon, WeaponAdmin)
admin.site.register(Pistol, WeaponAdmin)

# Регистрация подклассов брони
admin.site.register(Helmet, ArmorAdmin)
admin.site.register(BodyArmor, ArmorAdmin)
admin.site.register(LimbProtection, ArmorAdmin)