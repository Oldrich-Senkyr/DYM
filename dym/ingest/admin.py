from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import IngestedData

@admin.register(IngestedData)
class IngestedDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'received_at')
    ordering = ('-received_at',)
