from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='наименование')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('pk',)


class Material(models.Model):
    name = models.CharField(max_length=255, verbose_name='наименование', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='materials', **NULLABLE)
    code = models.CharField(max_length=50, unique=True, verbose_name='код', **NULLABLE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='стоимость', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
        ordering = ('pk',)
