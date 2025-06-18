from django.urls import path
from main.views import *
from . import views

urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path("catalog/", catalog, name="catalog"),
    path("all-creaters/", api_get_all_Creaters, name="api_all_creaters"),
    path('about/', about, name='about'),
    # Аутентификация
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout_view, name='logout'),
    path('account/<int:user_id>/', views.account, name='account'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/checkout/', views.checkout, name='checkout'),
]

