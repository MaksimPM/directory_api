from rest_framework import serializers
from directory.models import Material, Category
from django.db.models import Sum


# Сериализатор для материалов
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'category', 'code', 'cost']


# Сериализатор для категорий
class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        # Возвращаем вложенные категории для отображения дерева
        children = obj.children.all()
        return CategorySerializer(children, many=True).data


class CategoryWithTotalCostSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'total_cost', 'materials', 'children']

    def get_children(self, obj):
        # Рекурсивно получаем вложенные категории
        children = obj.children.all()
        return CategoryWithTotalCostSerializer(children, many=True).data

    def get_total_cost(self, obj):
        # Суммируем стоимость всех материалов в данной категории и вложенных
        total_cost = obj.materials.aggregate(Sum('cost'))['cost__sum'] or 0
        total_cost += self._get_children_cost(obj)
        return total_cost

    def _get_children_cost(self, obj):
        # Рекурсивно считаем стоимость всех вложенных материалов
        total_cost = 0
        for child in obj.children.all():
            total_cost += child.materials.aggregate(Sum('cost'))['cost__sum'] or 0
            total_cost += self._get_children_cost(child)
        return total_cost

    def get_materials(self, obj):
        # Возвращаем все материалы, связанные с данной категорией
        materials = obj.materials.all()
        return MaterialSerializer(materials, many=True).data
