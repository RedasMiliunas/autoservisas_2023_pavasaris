from django.contrib import admin
from .models import (Automobilis,
                     AutomobilioModelis,
                     Paslauga,
                     Uzsakymas,
                     UzsakymoEilute)

class OrderLineInline(admin.TabularInline):
    model = UzsakymoEilute
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['automobilis', 'data']
    inlines = [OrderLineInline]

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['automobilio_modelis', 'kliento_vardas', 'vin', 'valstybinis_nr']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['pavadinimas', 'kaina']

# Register your models here.
admin.site.register(Automobilis, VehicleAdmin)
admin.site.register(AutomobilioModelis)
admin.site.register(Paslauga, ServiceAdmin)
admin.site.register(Uzsakymas, OrderAdmin)
admin.site.register(UzsakymoEilute)