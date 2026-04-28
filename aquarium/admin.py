from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'rupee_price', 'stock', 'image']
    list_editable = ['stock', 'image']          # edit stock & image right from the list page
    search_fields = ['name']
    ordering = ['name']

    fields = ['name', 'price', 'image', 'stock'] # controls what shows in the edit form

    def rupee_price(self, obj):
        return f"₹{obj.price // 100}"
    rupee_price.short_description = 'Price (₹)'
