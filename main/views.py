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
    Creater = request.GET.get("Creater")
    if (Creater):
        weapon = Weapon.objects.filter(Creater=Creater)
    else:
        weapon = Weapon.objects.all()
    return render(request, "catalog.html", {"weapon": weapon})

def api_get_all_Creaters(request):
    creater = Creater.objects.all()
    dataList = [creater.parse_object() for creater in creater]
    # safe - чтобы отправить в качестве ответа массив, а не объект, как этого требует JsonResponse
    return JsonResponse(dataList, safe=False)
    
