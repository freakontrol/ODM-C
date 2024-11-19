from rest_framework import serializers
from .models import PartCategory, DocumentCategory, Part, Manufacturer, PurchaseOption, Container, Document

class PartCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PartCategory
        fields = ['id', 'name', 'description', 'url']
        
class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    #category = DocumentCategorySerializer()

    class Meta:
        model = Document
        fields = ['id', 'document_number', 'description', 'checked', 'doc_file', 'link', 'obsolete', 'category', 'item_number', 'revision', 'creation_date', 'url']

class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields = ['id', 'part_a', 'part_b', 'quantity', 'creation_date', 'url']
        
class ContainerASerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields = ['part_b', 'quantity', 'creation_date']

class ContainerBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields = ['part_a', 'quantity', 'creation_date']

class PartSerializer(serializers.HyperlinkedModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    
    containers_as_part_a = ContainerASerializer(many=True, read_only=True)
    containers_as_part_b = ContainerBSerializer(many=True, read_only=True)
    
    internal_part_number = serializers.CharField(max_length=255, required=False)
    item_number = serializers.IntegerField(required=False)
    variant = serializers.IntegerField(required=False)
    revision = serializers.IntegerField(required=False)

    class Meta:
        model = Part
        fields = ['id', 'internal_part_number', 'description', 'released', 'purchase_option', 'repository_link', 'documents', 'storage_code', 'creation_date', 'containers_as_part_a', 'containers_as_part_b', 'category', 'item_number', 'variant', 'revision', 'url']
class DocumentCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = ['id', 'name', 'description', 'url']

class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'contact_info', 'url']

class PurchaseOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PurchaseOption
        fields = ['id', 'part_ipn', 'manufacturer', 'manufacturer_code', 'datasheet', 'obsolete', 'url']
