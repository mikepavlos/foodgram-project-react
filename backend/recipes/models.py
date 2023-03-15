from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
