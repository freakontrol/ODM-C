from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PartViewSet, PartCategoryViewSet, DocumentCategoryViewSet, ManufacturerViewSet,
                    PurchaseOptionViewSet, ContainerViewSet, DocumentViewSet, BomViewSet)
from . import views

router = DefaultRouter()
router.register(r'parts', PartViewSet, basename='part')
router.register(r'boms', BomViewSet, basename='bom')
router.register(r'part-categories', PartCategoryViewSet, basename='partcategory')
router.register(r'document-categories', DocumentCategoryViewSet, basename='documentcategory')
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'purchase-options', PurchaseOptionViewSet, basename='purchaseoption')
router.register(r'containers', ContainerViewSet, basename='container')
router.register(r'documents', DocumentViewSet, basename='document')
#router.register(r'part-documents', PartDocumentViewSet, basename='partdocument')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]