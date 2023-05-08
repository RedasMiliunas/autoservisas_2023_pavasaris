from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.paginator import Paginator

# Create your views here.

from django.db.models import Q

def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(Q(valstybinis_nr__icontains=query) | Q(vin__icontains=query) | Q(kliento_vardas__icontains=query) | Q(automobilio_modelis__marke__icontains=query) | Q(automobilio_modelis__modelis__icontains=query))
    return render(request, 'search.html', {'vehicles': search_results, 'query': query})

def index(request):
    #sesijos (fiksuota info be jo prisijungimu: fiksuojam skaiciuka kiek kartu jis prisijungia:
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'service_count': Paslauga.objects.count(),
        'orders_done': Uzsakymas.objects.filter(status__exact='i').count(),
        'vehicles': Automobilis.objects.count(),
        'num_visits': num_visits,

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

from django.views.generic.edit import FormMixin
from .forms import OrderReviewForm
class OrderDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = 'order.html'
    context_object_name = 'order'
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.komentatorius = self.request.user
        form.save()
        return super().form_valid(form)


from django.contrib.auth.mixins import LoginRequiredMixin

class MyOrdersListview(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    context_object_name = 'my_orders'
    template_name = 'my_orders.html'

    def get_queryset(self):
        return Uzsakymas.objects.filter(klientas=self.request.user)


from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import User
from django.contrib import messages

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} uzimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. pastu {email} jau uzregistruotas')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} sekmingai uzregistruotas')
                    return redirect('login')
        else:
            messages.error(request, f'Slaptazodziai nesutampa!')
            return redirect('register')

    else:
        return render(request, 'registration/register.html')