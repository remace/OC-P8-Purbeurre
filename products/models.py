"""
models for products app
"""

from django.db import models
from accounts.models import User


class Product(models.Model):
    ''' Product model, as should be stored in database'''
    NUTRISCORE_CHOICES=[
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('F','inconnu'),
    ]

    ENERGY_UNITS=[
        ('kJ','kJ'),
        ('kcal', 'kcal'),
    ]

    name = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=1, choices=NUTRISCORE_CHOICES, default='F')

    # with django datetimes
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    # nutritionnal values per 100g
    energy_unit = models.CharField(max_length=6, choices=ENERGY_UNITS, default = 'kcal')
    energy_100g = models.DecimalField(max_digits=10,
                                        decimal_places=3,
                                        null=True,
                                        blank=True,
                                        default=0)
    carbohydrates_100g = models.DecimalField(max_digits=6,
                                            decimal_places=3,
                                            null=True,
                                            blank=True,
                                            default=0)
    sugars_100g = models.DecimalField(max_digits=6,
                                        decimal_places=3,
                                        null=True,
                                        blank=True,
                                        default=0)
    fat_100g = models.DecimalField(max_digits=6,
                                        decimal_places=3,
                                        null=True,
                                        blank=True,
                                        default=0)
    saturated_fat_100g = models.DecimalField(max_digits=6,
                                                decimal_places=3,
                                                null=True,
                                                blank=True,
                                                default=0)
    fiber_100g = models.DecimalField(max_digits=6,
                                        decimal_places=3,
                                        null=True,
                                        blank=True,
                                        default=0)
    proteins_100g = models.DecimalField(max_digits=6,
                                            decimal_places=3,
                                            null=True,
                                            blank=True,
                                            default=0)
    salt_100g = models.DecimalField(max_digits=6,
                                        decimal_places=3,
                                        null=True,
                                        blank=True,
                                        default=0)
    sodium_100g = models.DecimalField(max_digits=6,
                                        decimal_places=3,
                                        null=True,
                                        blank=True,
                                        default=0)

    # link to open food facts page
    off_link = models.CharField(max_length=1024)
    off_thumb_link = models.CharField(max_length=1024,
                                        null=True)
    off_img_link = models.CharField(max_length=1024,
                                        null=True)

    category = models.ForeignKey('Category', null=False, on_delete=models.CASCADE)

    # favourites saving
    in_users_favourites = models.ManyToManyField(User,related_name='users',blank=False)


class Category(models.Model):
    ''' category model as should be stored in database'''
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'
 