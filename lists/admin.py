from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    list_display = ("__str__", "count_rooms")
    filter_horizontal = ("rooms",)
