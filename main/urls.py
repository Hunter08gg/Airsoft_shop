from django.urls import path
from main.views import *

urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path("catalog/", catalog, name="catalog"),
 path("all-creaters/", api_get_all_Creaters, name="api_all_creaters"),
]

