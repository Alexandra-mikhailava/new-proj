from django.contrib import admin
from .models import Client, Employee, Service, Appointment

# Register your models here.
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(Appointment)