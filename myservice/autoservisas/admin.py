from django.contrib import admin
from .models import (Automobilis,
                     AutomobilioModelis,
                     Paslauga,
                     Uzsakymas,
                     UzsakymoEilute,
                     OrderReview,
                     Profilis)

class OrderLineInline(admin.TabularInline):
    model = UzsakymoEilute
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['automobilis', 'data', 'grazinimo_data', 'status']
    list_editable = ['grazinimo_data', 'status']
    inlines = [OrderLineInline]

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['automobilio_modelis', 'kliento_vardas', 'vin', 'valstybinis_nr']
    list_filter = ['kliento_vardas', 'automobilio_modelis__marke', 'automobilio_modelis__modelis']
    search_fields = ['vin', 'valstybinis_nr', 'automobilio_modelis__marke', 'automobilio_modelis__modelis']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['pavadinimas', 'kaina']


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['uzsakymas', 'komentatorius', 'sukurimo_data', 'komentaras']

# Register your models here.
admin.site.register(Automobilis, VehicleAdmin)
admin.site.register(AutomobilioModelis)
admin.site.register(Paslauga, ServiceAdmin)
admin.site.register(Uzsakymas, OrderAdmin)
admin.site.register(UzsakymoEilute)
admin.site.register(OrderReview, OrderReviewAdmin)
admin.site.register(Profilis)