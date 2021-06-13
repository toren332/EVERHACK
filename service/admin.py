from django.contrib import admin
from service import models


@admin.register(models.Building)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'point']


@admin.register(models.Poly)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'polygon', 'business_kind']