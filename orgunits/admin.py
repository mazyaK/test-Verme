from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin, register

from orgunits.models import Organization


@register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ("id", "name", "code", "parent_name")
    fields = ("name", "code", "parent")

    def parent_name(self, obj):
        return obj.parent.name if obj.parent is not None else None

    parent_name.short_description = "Вышестоящая организация"
