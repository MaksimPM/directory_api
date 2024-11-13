from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Material, Category
from .serializers import MaterialSerializer, CategorySerializer
import pandas as pd


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @action(detail=False, methods=['post'])
    def upload_excel(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "Файл не предоставлен"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                category, _ = Category.objects.get_or_create(name=row['Категория'], code=row['Код категории'])
                Material.objects.create(
                    name=row['Материал'],
                    category=category,
                    code=row['Код'],
                    cost=row['Стоимость']
                )
            return Response({"status": "Материал успешно импортирован"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
