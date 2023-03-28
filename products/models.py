from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse


class Category(models.Model):
    """ Model for product categories"""

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def get_url(self):
        return reverse('products_by_category', args=[self.name])

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


VARIANTS = (('None', 'None'),
            ('Size', 'Size'),
            ('Colour', 'Colour'),
            ('Size-Colour', 'Size-Colour'),
            )


class Product(models.Model):
    """Model for product information"""

    class Meta:
        verbose_name_plural = 'Products'

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, default=None, unique=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    rating = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_alt = models.CharField(max_length=254, null=True, blank=True)
    variant_options = models.CharField(max_length=15, choices=VARIANTS, default='Size-Colour')
    wishlist = models.ManyToManyField(User, related_name="wishlist", blank=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


class Colour(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def colour_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Colour</p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class ImageVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=True)
    image_variant_alt = models.CharField(max_length=50, blank=True)
    # image_variant_url = models.URLField(max_length=1024, null=True, blank=True)
    image_variant = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Variant(models.Model):
    title = models.CharField(max_length=120)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour,on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    amount_in_stock = models.IntegerField()
    sale = models.BooleanField(default=False)
    discounted_price = models.DecimalField(
        max_digits=6, decimal_places=0, null=True, blank=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = ImageVariant.objects.get(id=self.image_id)
        if img.id is not None:
            varimage_variant = img.image_variant.url
        else:
            varimage_variant = ""
        return varimage_variant

    def image_tag(self):
        img = ImageVariant.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image_variant.url))
        else:
            return ""


""" DNL Bowers"""
# def get_rating(self):
#         """Calculates the overall rating for the product"""

#         if self.number_of_ratings == 0:
#             return 0
#         else:
#             self.current_rating = round(
#                 self.accumulative_rating / self.number_of_ratings, 2)
#             return self.current_rating

#     def save(self, *args, **kwargs):
#         """
#         Override the original save method to set the price
#         according to if it has a sale or not
#         """
#         self.get_rating()

#         if self.stock_level <= 0:
#             self.in_stock = False
#         else:
#             self.in_stock = True

#         self.slug = slugify(self.name)

#         if self.has_sale:
#             self.price = self.discounted_price
#         else:
#             self.price = self.rrp

#         super().save(*args, **kwargs)
