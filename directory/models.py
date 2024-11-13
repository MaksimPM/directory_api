from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='наименование')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    code = models.CharField(max_length=50, unique=True, verbose_name='код')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('pk',)

    def total_cost(self):
        total = sum(material.cost for material in self.materials.all())
        for child in self.children.all():
            total += child.total_cost()
        return total


class Material(models.Model):
    name = models.CharField(max_length=255, verbose_name='наименование')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='materials')
    code = models.CharField(max_length=50, unique=True, verbose_name='код')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='стоимость')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
        ordering = ('pk',)
