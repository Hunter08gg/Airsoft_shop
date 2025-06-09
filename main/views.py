from django.shortcuts import render
from main.models import Weapon, Creater
from django.views.generic import ListView
from django.http import HttpRequest, JsonResponse

class IndexListView (ListView):
    model = Weapon
    template_name = "index.html"
    context_object_name = "weapons"

def catalog(request: HttpRequest):
    # Достаю параметр маршрута
    creater = request.GET.get("creater")
    if (creater):
        weapon = Weapon.objects.filter(creaters=creater)
    else:
        weapon = Weapon.objects.all()
    return render(request, "catalog.html", {"weapons": weapon})

def api_get_all_Creaters(request):
    creaters = Creater.objects.all()
    dataList = [creater.parse_object() for creater in creaters]
    # safe - чтобы отправить в качестве ответа массив, а не объект, как этого требует JsonResponse
    return JsonResponse(dataList, safe=False)
    
