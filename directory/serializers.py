from rest_framework import serializers
from .models import Material, Category


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'category', 'code', 'cost']


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    materials = MaterialSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'code', 'children', 'materials', 'total_cost']

    @staticmethod
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children, many=True).data
        return []

    @staticmethod
    def get_total_cost(self, obj):
        return obj.total_cost()
