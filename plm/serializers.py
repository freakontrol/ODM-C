from rest_framework import serializers
from .models import PartCategory, DocumentCategory, Part, Manufacturer, PurchaseOption, Container, Document, PartDocument

class PartCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PartCategory
        fields = ['id', 'name', 'description']

class DocumentCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = ['id', 'name', 'description']

class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'contact_info']

class PartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Part
        fields = ['url', 'internal_part_number', 'description', 'released', 'purchase_option', 'repository_link', 'storage_code', 'creation_date', 'category', 'item_number', 'variant', 'revision']

    extra_kwargs = {
        'url': {'view_name': 'part-detail', 'lookup_field': 'internal_part_number'}
    }
class PurchaseOptionSerializer(serializers.HyperlinkedModelSerializer):
    part_ipn = PartSerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = PurchaseOption
        fields = ['id', 'part_ipn', 'manufacturer', 'manufacturer_code', 'datasheet', 'obsolete']

class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    part_a = PartSerializer()
    part_b = PartSerializer()

    class Meta:
        model = Container
        fields = ['id', 'part_a', 'part_b', 'quantity', 'creation_date']

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    category = DocumentCategorySerializer()

    class Meta:
        model = Document
        fields = ['id', 'document_number', 'description', 'checked', 'doc_file', 'link', 'obsolete', 'category', 'item_number', 'revision', 'creation_date']  # add other fields as needed

class PartDocumentSerializer(serializers.HyperlinkedModelSerializer):
    part = PartSerializer()
    document = DocumentSerializer()

    class Meta:
        model = PartDocument
        fields = ['id', 'part', 'document']