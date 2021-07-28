from django.contrib import admin

from .models import EumcDrugData


@admin.register(EumcDrugData)
class EumcDrugDataAdmin(admin.ModelAdmin):
    list_display = 'rawdata', 'location', 'created',
    