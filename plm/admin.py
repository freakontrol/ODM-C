from django.contrib import admin

# Register your models here.
from .models import Plm

class PlmAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    
    class Meta:
        model = Plm
        
admin.site.register(Plm, PlmAdmin)