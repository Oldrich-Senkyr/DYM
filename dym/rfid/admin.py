from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import RFIDCard, Permission, CardPermission, RFIDLog

@admin.register(RFIDCard)
class RFIDCardAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'person', 'valid_from', 'valid_to')
    search_fields = ('card_id', 'person__first_name', 'person__last_name')
    list_filter = ('valid_from', 'valid_to')

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CardPermission)
class CardPermissionAdmin(admin.ModelAdmin):
    list_display = ('card', 'permission')

@admin.register(RFIDLog)
class RFIDLogAdmin(admin.ModelAdmin):
    list_display = ('card', 'event', 'timestamp')
    list_filter = ('timestamp', 'event')
    search_fields = ('card__card_id', 'event')
