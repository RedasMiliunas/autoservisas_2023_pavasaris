from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    context = {
        'service_count': Paslauga.objects.count(),
        'orders_done': Uzsakymas.objects.filter(status__exact='i').count(),
        'vehicles': Automobilis.objects.count(),

    }
    return render(request, 'index.html', context=context)

    # return HttpResponse("Mano autoservisas")

    # context = {
    #     'paslaugos_count' = Paslauga.objects.count(),
    #     'uzsakymas_done' = Uzsakymas.objects.count(),
    #     'vihicle' = Automobilis.objects.filter(status__exact='v').count(),    # 'v' = 'Vykdoma'
    # }

    # return render(request, 'autoservice.html', context=context)

# Django V-tos dalies:

def vehicles(request):
    paginator = Paginator(Automobilis.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_vehicles = paginator.get_page(page_number)
    context = {
        'vehicles': paged_vehicles
    }
    # context = {
    #     'vehicles': Automobilis.objects.all()
    # }
    return render(request, 'vehicles.html', context=context)
#OR:
# def vehicles(request):
    #return render(request, 'vehicles.html', context={'vehicles': Automobilis.objects.all()})


# def vehicles(request):
#     context = {
#         'vehicles': Automobilis.objects.all()
#     }
#     return render(request, 'vehicles.html', context=context)

#2uzduotis:
def vehicle(request, vehicle_id):
    context = {
        'vehicle': get_object_or_404(Automobilis, pk=vehicle_id)
    }
    return render(request, 'vehicle.html', context=context)

#AAAA
class OrderListView(generic.ListView):
    model = Uzsakymas
    template_name = 'orders.html'
    context_object_name = 'orders'
    paginate_by = 2

class OrderDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'order.html'
    context_object_name = 'order'
