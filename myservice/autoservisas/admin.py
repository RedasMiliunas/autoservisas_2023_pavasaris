from django.contrib import admin
from .models import (Automobilis,
                     AutomobilioModelis,
                     Paslauga,
                     Uzsakymas,
                     UzsakymoEilute)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['']


# Register your models here.
admin.site.register(Automobilis)
admin.site.register(AutomobilioModelis)
admin.site.register(Paslauga)
admin.site.register(Uzsakymas, OrderAdmin)
admin.site.register(UzsakymoEilute)