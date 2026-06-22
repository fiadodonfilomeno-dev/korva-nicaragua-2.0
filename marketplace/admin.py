from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'price', 'category', 'is_active', 'views_count', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'user__business_name']
    actions = ['activate_products', 'deactivate_products']
    
    def activate_products(self, request, queryset):
        queryset.update(is_active=True)
    activate_products.short_description = "Activar productos seleccionados"
    
    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_products.short_description = "Desactivar productos seleccionados"
