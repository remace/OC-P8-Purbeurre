from django.contrib import admin

from products.models import Product, Category


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name',
                    'nutriscore',
                    'category',
                    'energy_100g',
                    'carbohydrates_100g',
                    'sugars_100g',
                    'fat_100g',
                    'saturated_fat_100g',
                    'fiber_100g',
                    'proteins_100g',
                    'sodium_100g',
                    'off_link'
      )
    list_filter = ('category', 'nutriscore',)
    search_fields = ('name', )

@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name', )
    inlines = (ProductInline, )


