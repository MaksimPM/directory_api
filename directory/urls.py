from django.urls import path, include
from rest_framework.routers import DefaultRouter

from directory.apps import DirectoryConfig
from .views import MaterialViewSet, CategoryViewSet, UploadMaterialsView, CategoryWithCostViewSet


app_name = DirectoryConfig.name

router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'categories_with_cost', CategoryWithCostViewSet, basename='category_with_cost')

urlpatterns = [
    path('upload_materials/', UploadMaterialsView.as_view(), name='upload_materials'),
    path('', include(router.urls)),
]
