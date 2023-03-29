from django.contrib import admin
from .models import (Product, Category, Size, Colour,
                     ImageVariant, Variant, ProductReview)

import admin_thumbnails


@admin_thumbnails.thumbnail('image_variant')
class ImageVariantAdminInline(admin.TabularInline):
    """Enables editing of Image Variations from Admin"""
    model = ImageVariant
    readonly_fields = ('id',)
    extra = 1


class VariantAdminInline(admin.TabularInline):
    """Enables editing of Product Variations from Admin"""
    model = Variant
    readonly_fields = ('image_tag',)
    extra = 1


@admin_thumbnails.thumbnail('image')
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = (VariantAdminInline, ImageVariantAdminInline)
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
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


class ColourAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'colour_tag'
    )


class VariantAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'colour',
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
admin.site.register(Colour, ColourAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ImageVariant, ImageVariantAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(ProductReview)
