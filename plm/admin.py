# admin.py
from django.contrib import admin
from .models import PartCategory, DocumentCategory, Part, Manufacturer, PurchaseOption, Container, Document

@admin.register(PartCategory)
class PartCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('internal_part_number', 'description', 'released', 'category')

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')

@admin.register(PurchaseOption)
class PurchaseOptionAdmin(admin.ModelAdmin):
    list_display = ('part_ipn', 'manufacturer', 'obsolete')

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('part_a', 'part_b', 'quantity', 'creation_date')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'description', 'checked', 'category', 'obsolete')

# @admin.register(PartDocument)
# class PartDocumentAdmin(admin.ModelAdmin):
#     list_display = ('part', 'document')
