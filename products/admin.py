from django.contrib import admin
from .models import (Product, Category, Size, Color,
                     ImageVariant, ProductAttribute, ProductReview)

import admin_thumbnails


@admin_thumbnails.thumbnail('image_variant')
class ImageVariantAdminInline(admin.TabularInline):
    """Enables editing of Image Variations from Admin"""
    model = ImageVariant
    readonly_fields = ('id',)
    extra = 1


class ProductAttributeAdminInline(admin.TabularInline):
    """Enables editing of Product Variations from Admin"""
    model = ProductAttribute
    readonly_fields = ('image_tag',)
    extra = 1


@admin_thumbnails.thumbnail('image')
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ProductAttributeAdminInline, ImageVariantAdminInline)
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'image_tag',
    )

    ordering = ('sku',)

    search_fields = (
        'name',
        'description',
        'sku',
        'category',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class SizeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
    )


class ColorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'color_tag'
    )


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'color',
        'size',
        'in_stock',
        'amount_in_stock',
        'sale',
        'discounted_price',
        'image_tag',
    )


@admin_thumbnails.thumbnail('image_variant')
class ImageVariantAdmin(admin.ModelAdmin):
    list_display = (
            'product',
            'image_variant',
            'image_variant_thumbnail',
        )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ImageVariant, ImageVariantAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductReview)
