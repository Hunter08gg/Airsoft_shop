from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpRequest, JsonResponse
from main.models import (
    Creater, 
    Weapon, AssaultRifle, SniperRifle, MachineGun, Shotgun, MeleeWeapon, Pistol,
    Armor, Helmet, BodyArmor, LimbProtection,
    Accessory
)

class IndexListView(ListView):
    model = Weapon
    template_name = "index.html"
    context_object_name = "weapons"

def catalog(request: HttpRequest):
    # Получаем параметры фильтрации
    category = request.GET.get("category")
    creater_id = request.GET.get("creater")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    # Фильтрация по категории
    if category == "weapon":
        items = Weapon.objects.all()
    elif category == "armor":
        items = Armor.objects.all()
    elif category == "accessory":
        items = Accessory.objects.all()
    else:
        # Если категория не указана, показываем все товары
        items = list(Weapon.objects.all()) + list(Armor.objects.all()) + list(Accessory.objects.all())

    # Фильтрация по производителю
    if creater_id:
        if isinstance(items, list):
            items = [item for item in items if item.creator and item.creator.id == int(creater_id)]
        else:
            items = items.filter(creator__id=creater_id)

    # Фильтрация по цене
    if price_min:
        if isinstance(items, list):
            items = [item for item in items if item.price >= float(price_min)]
        else:
            items = items.filter(price__gte=float(price_min))
    
    if price_max:
        if isinstance(items, list):
            items = [item for item in items if item.price <= float(price_max)]
        else:
            items = items.filter(price__lte=float(price_max))

    # Получаем всех производителей для фильтра
    creators = Creater.objects.all()

    context = {
        'items': items,
        'creators': creators,
    }
    return render(request, "catalog.html", context)

def api_get_all_Creaters(request):
    creators = Creater.objects.all()
    dataList = [creator.parse_object() for creator in creators]
    return JsonResponse(dataList, safe=False)
