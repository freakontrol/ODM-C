# serializers.py
from rest_framework import serializers
from .models import PartCategory, DocumentCategory, Part, Manufacturer, PurchaseOption, Container, Document, PartDocument

class PartCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartCategory
        fields = '__all__'