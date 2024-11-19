from rest_framework import generics, viewsets, pagination, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from .models import PartCategory, DocumentCategory, Part, Manufacturer, PurchaseOption, Container, Document
from .serializers import PartCategorySerializer, DocumentCategorySerializer, PartSerializer, ManufacturerSerializer, PurchaseOptionSerializer, ContainerSerializer, DocumentSerializer

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class ModelViewSetWithPaginationAndPermissions(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    #permission_classes = [permissions.IsAuthenticated]

class PartViewSet(ModelViewSetWithPaginationAndPermissions):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    #lookup_field = 'internal_part_number'
    
    @action(detail=True, methods=['post'])
    def add_document(self, request, pk=None):
        part = self.get_object()
        document_id = request.data.get('document_id')

        try:
            document = Document.objects.get(id=document_id)
            part.documents.add(document)
            return Response({'status': 'Document added to the part'}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_document(self, request, pk=None):
        part = self.get_object()
        document_id = request.data.get('document_id')

        try:
            document = Document.objects.get(id=document_id)
            part.documents.remove(document)
            return Response({'status': 'Document removed from the part'}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

class PartCategoryViewSet(ModelViewSetWithPaginationAndPermissions):
    queryset = PartCategory.objects.all()
    serializer_class = PartCategorySerializer

class DocumentCategoryViewSet(ModelViewSetWithPaginationAndPermissions):
    queryset = DocumentCategory.objects.all()
    serializer_class = DocumentCategorySerializer

class ManufacturerViewSet(ModelViewSetWithPaginationAndPermissions):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class PurchaseOptionViewSet(ModelViewSetWithPaginationAndPermissions):
    queryset = PurchaseOption.objects.all()
    serializer_class = PurchaseOptionSerializer

class ContainerViewSet(ModelViewSetWithPaginationAndPermissions):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

class DocumentViewSet(ModelViewSetWithPaginationAndPermissions):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_field = 'document_number'