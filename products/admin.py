from django.contrib import admin
from .models import (Product, Category, Size, Colour,
                     ImageVariant, ProductVariant)

import admin_thumbnails


class ProductVariantAdminInline(admin.TabularInline):
    """Enables editing of Product Variations from Admin"""
    model = ProductVariant


class ImageVariantAdminInline(admin.TabularInline):
    """Enables editing of Image Variations from Admin"""
    model = ImageVariant
    readonly_fields = ('id',)


@admin_thumbnails.thumbnail('image')
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductVariantAdminInline, ImageVariantAdminInline)
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image_tag',
    )

    # readonly_fields = ('image_tag',)

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


class ColourAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'colour_tag'
    )


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'colour',
        'size',
        'in_stock',
        'amount_in_stock',
        'sale',
        'discounted_price',
        'image_id',
    )


# @admin_thumbnails.thumbnail('image_variant')
class ImageVariantAdmin(admin.ModelAdmin):
        list_display = (
                'product',
                'alt',
                'image_variant',
                # 'image_thumbnail',
            )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Colour, ColourAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ImageVariant, ImageVariantAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
