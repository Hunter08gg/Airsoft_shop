import json
from venv import logger
from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
import logging
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import BaseItem,  Creater, Profile 
from django.contrib import messages
from .models import Cart, CartItem
from django.http import HttpRequest, JsonResponse
from main.models import (
    Creater, 
    Weapon, AssaultRifle, SniperRifle, MachineGun, Shotgun, MeleeWeapon, Pistol,
    Armor, Helmet, BodyArmor, LimbProtection,
    Accessory, Order
)
from django.contrib.contenttypes.models import ContentType
ContentType.objects.get_for_model(Helmet)
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
    subcategory = request.GET.get("subcategory")
    creater_id = request.GET.get("creater")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    # Фильтрация по категории и подкатегории
    if category == "weapon":
        if subcategory == "assault":
            items = AssaultRifle.objects.all()
        elif subcategory == "sniper":
            items = SniperRifle.objects.all()
        elif subcategory == "machinegun":
            items = MachineGun.objects.all()
        elif subcategory == "shotgun":
            items = Shotgun.objects.all()
        elif subcategory == "pistol":
            items = Pistol.objects.all()
        elif subcategory == "melee":
            items = MeleeWeapon.objects.all()
        else:
            items = Weapon.objects.all()
    elif category == "armor":
        if subcategory == "helmet":
            items = Helmet.objects.all()
        elif subcategory == "body":
            items = BodyArmor.objects.all()
        elif subcategory == "limb":
            items = LimbProtection.objects.all()
        else:
            items = Armor.objects.all()
    elif category == "accessory":
        items = Accessory.objects.all()
    else:
        # Для случая "Все товары" используем union всех конкретных моделей
        items = list(Weapon.objects.all()) + \
                list(Armor.objects.all()) + \
                list(Accessory.objects.all())

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

    context = {
        'items': items,
        'creators': Creater.objects.all(),
        'current_category': category,
        'current_subcategory': subcategory,
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
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    cart_items = []
    total_price = 0
    
    for cart_item in cart.items.all():
        try:
            item = cart_item.item
            if item:
                item_total = cart_item.quantity * item.price
                cart_items.append({
                    'cart_item': cart_item,
                    'item': item,
                    'total_price': item_total
                })
                total_price += item_total
        except:
            cart_item.delete()
    
    return render(request, 'cart.html', {
        'cart': cart,
        'items': cart_items,
        'total_price': total_price
    })

@login_required
def add_to_cart(request, item_id):
    try:
        # Получаем данные из запроса
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
            category = data.get('category')
        else:
            category = request.POST.get('category')

        # Определяем модель по категории
        model_map = {
            'weapon': [Weapon, AssaultRifle, SniperRifle, MachineGun, Shotgun, MeleeWeapon, Pistol],
            'armor': [Armor, Helmet, BodyArmor, LimbProtection],
            'accessory': [Accessory]
        }

        item = None
        for model in model_map.get(category, []):
            try:
                item = model.objects.get(pk=item_id)
                break
            except model.DoesNotExist:
                continue

        if not item:
            raise BaseItem.DoesNotExist("Товар не найден")

        # Проверяем соответствие категории
        expected_category = None
        if isinstance(item, (Helmet, BodyArmor, LimbProtection)):
            expected_category = 'armor'
        elif isinstance(item, (AssaultRifle, SniperRifle, MachineGun, Shotgun, MeleeWeapon, Pistol)):
            expected_category = 'weapon'
        elif isinstance(item, Accessory):
            expected_category = 'accessory'

        if expected_category and expected_category != category:
            raise ValueError(f"Несоответствие категории: ожидается {expected_category}, получено {category}")

        # Добавляем в корзину
        cart, created = Cart.objects.get_or_create(user=request.user)
        content_type = ContentType.objects.get_for_model(item.__class__)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            content_type=content_type,
            object_id=item.id,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({
            'success': True,
            'message': f"Товар {item.name} добавлен в корзину",
            'cart_count': cart.items.count()
        })
            
    except Exception as e:
        logger.error(f"Ошибка добавления в корзину: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    


# Добавим функцию для AJAX обновления количества
@login_required
def update_cart_item_ajax(request, item_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            cart_item = CartItem.objects.get(pk=item_id, cart__user=request.user)
            quantity = int(request.POST.get('quantity', 1))
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                
                # Получаем обновленные данные корзины
                cart = cart_item.cart
                total_price = sum(
                    item.quantity * item.item.price 
                    for item in cart.items.all() 
                    if hasattr(item, 'item')
                )
                
                return JsonResponse({
                    'success': True,
                    'quantity': cart_item.quantity,
                    'item_total': cart_item.quantity * cart_item.item.price,
                    'cart_total': total_price
                })
            else:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'deleted': True
                })
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
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

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(pk=item_id, cart__user=request.user)
        cart_item.delete()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Получаем обновленные данные корзины
            cart = request.user.cart
            total_price = sum(
                item.quantity * item.item.price 
                for item in cart.items.all()
                if hasattr(item, 'item') )
            
            return JsonResponse({
                'success': True,
                'message': 'Товар удален из корзины',
                'cart_total': total_price,
                'cart_count': cart.items.count()
            })
        else:
            messages.success(request, "Товар удален из корзины")
            return redirect('cart')
            
    except CartItem.DoesNotExist:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'Товар не найден в корзине'
            }, status=404)
        else:
            messages.error(request, "Товар не найден в корзине")
            return redirect('cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, "Ваша корзина пуста")
        return redirect('cart')
    
    if request.method == 'POST':
        # Создаем заказ
        total_price = sum(item.total_price for item in cart.items.all())
        order = Order.objects.create(
            user=request.user,
            total_price=total_price
        )
        order.items.set(cart.items.all())
        
        # Очищаем корзину
        cart.items.all().delete()
        
        messages.success(request, "Ваш заказ успешно оформлен!")
        return redirect('order_detail', order_id=order.id)
    
    total_price = sum(item.total_price for item in cart.items.all())
    return render(request, 'checkout.html', {
        'cart': cart,
        'total_price': total_price
    })

@login_required
def cart_count(request):
    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.items.count()
    except Cart.DoesNotExist:
        count = 0
    
    return JsonResponse({'count': count})

@login_required
def cart_total(request):
    try:
        cart = Cart.objects.get(user=request.user)
        total = sum(
            item.quantity * item.item.price 
            for item in cart.items.all() 
            if hasattr(item, 'item')
        )
    except Cart.DoesNotExist:
        total = 0
    
    return JsonResponse({'total': total})

def get_item_category(item):
    if isinstance(item, (Helmet, BodyArmor, LimbProtection)):
        return 'armor'
    elif isinstance(item, (AssaultRifle, SniperRifle, ...)):
        return 'weapon'
    
    