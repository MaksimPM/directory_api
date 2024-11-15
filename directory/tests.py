import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Material
from openpyxl import Workbook
from io import BytesIO


@pytest.mark.django_db
class TestCategoryMaterialAPI:

    def setup_method(self):
        self.client = APIClient()

    def test_upload_materials(self):
        url = reverse('directory:upload_materials')
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(['Материал', 'Категория', 'Код материала', 'Стоимость материала'])
        sheet.append(['Материал 1', 'Категория 1', 'Код 1', 100.0])
        sheet.append(['Материал 2', 'Категория 1', 'Код 2', 200.0])
        sheet.append(['Материал 3', 'Категория 2', 'Код 3', 300.0])

        file = BytesIO()
        workbook.save(file)
        file.seek(0)

        response = self.client.post(url, {'file': file}, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert Material.objects.count() == 3
        assert Category.objects.count() == 2

    def test_category_with_total_cost(self):
        root_category = Category.objects.create(name='Root Category')
        child_category_1 = Category.objects.create(name='Child Category 1', parent=root_category)
        child_category_2 = Category.objects.create(name='Child Category 2', parent=root_category)

        Material.objects.create(name='Material 1', category=root_category, cost=100.0)
        Material.objects.create(name='Material 2', category=child_category_1, cost=200.0)
        Material.objects.create(name='Material 3', category=child_category_2, cost=300.0)

        url = reverse('directory:category_with_cost-list')  # Убедитесь, что URL правильный
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        root_category_data = next(item for item in response.data if item['name'] == 'Root Category')
        assert root_category_data['total_cost'] == 600.0
        assert root_category_data['children'][0]['total_cost'] == 200.0
        assert root_category_data['children'][1]['total_cost'] == 300.0

    def test_hierarchy_structure(self):
        root_category = Category.objects.create(name='Комплектующие и запчасти')
        standard_parts = Category.objects.create(name='Детали стандартные', parent=root_category)
        fastening_items = Category.objects.create(name='Изделия крепежные', parent=root_category)
        Category.objects.create(name='Насосы', parent=standard_parts)
        Category.objects.create(name='Подшипники', parent=standard_parts)
        Category.objects.create(name='Болты', parent=fastening_items)
        Category.objects.create(name='Винты', parent=fastening_items)

        url = reverse('directory:category_with_cost-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        root_data = next(item for item in response.data if item['name'] == 'Комплектующие и запчасти')
        assert len(root_data['children']) == 2
        assert root_data['children'][0]['name'] == 'Детали стандартные'
        assert root_data['children'][1]['name'] == 'Изделия крепежные'
        assert len(root_data['children'][0]['children']) == 2
        assert len(root_data['children'][1]['children']) == 2
