from rest_framework import generics, viewsets, pagination, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from .models import PartCategory, DocumentCategory, Part, Manufacturer, PurchaseOption, Container, Document, PartDocument
from .serializers import PartCategorySerializer, DocumentCategorySerializer, PartSerializer, ManufacturerSerializer, PurchaseOptionSerializer, ContainerSerializer, DocumentSerializer, PartDocumentSerializer

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Parts':'/parts/'
    }
    return Response("API BASE POINT", safe=False)

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
    
    @action(detail=False, methods=['post'])
    def create_new(self, request):
        data = request.data
        part = Part()

        if 'variant' in data:
            part.create_new_variant(**data)
        elif 'revision' in data:
            part.create_new_revision(**data)
        else:
            part.create_new_item(**data)

        serializer = self.get_serializer(part)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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

class PartDocumentViewSet(ModelViewSetWithPaginationAndPermissions):
    queryset = PartDocument.objects.all()
    serializer_class = PartDocumentSerializer