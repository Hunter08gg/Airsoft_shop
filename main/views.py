from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import BaseItem,  Creater, Profile 
from django.contrib import messages
from .models import Cart, CartItem
from django.http import HttpRequest, JsonResponse
from main.models import (
    Creater, 
    Weapon, AssaultRifle, SniperRifle, MachineGun, Shotgun, MeleeWeapon, Pistol,
    Armor, Helmet, BodyArmor, LimbProtection,
    Accessory
)
def index(request):
    # Получаем все товары (включая подклассы) с предзагрузкой производителя
    items = BaseItem.objects.all().select_related('creator')
    return render(request, 'index.html', {'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(BaseItem, pk=item_id)
    return render(request, 'item_detail.html', {'item': item})

class IndexListView(ListView):
    model = Weapon
    template_name = "index.html"
    context_object_name = "weapons"


def about(request):
    creators = Creater.objects.all()
    return render(request, 'about.html', {'creators': creators})

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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаем профиль для нового пользователя
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('index')

@login_required
def account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'account.html', {'user': user, 'profile': profile})

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(BaseItem, pk=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"Товар {item.name} добавлен в корзину")
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Товар удален из корзины")
    return redirect('cart')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = request.POST.get('quantity', 1)
    
    try:
        quantity = int(quantity)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Количество обновлено")
        else:
            cart_item.delete()
            messages.success(request, "Товар удален из корзины")
    except ValueError:
        messages.error(request, "Некорректное количество")
    
    return redirect('cart')