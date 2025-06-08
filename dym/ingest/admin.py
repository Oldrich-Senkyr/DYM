from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import IngestedData, CardEvent

@admin.register(IngestedData)
class IngestedDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'received_at')
    ordering = ('-received_at',)


@admin.register(CardEvent)
class CardEventAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'card_number', 'event_type', 'object_id', 'reader_id')
    list_filter = ('event_type', 'object_id', 'reader_id')
    search_fields = ('card_number', 'object_id', 'reader_id')
    ordering = ('-timestamp',)