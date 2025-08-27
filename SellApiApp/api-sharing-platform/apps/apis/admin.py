from django.contrib import admin
from .models import Api

class ApiAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

admin.site.register(Api, ApiAdmin)