from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Count, Avg
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """ Model for product categories"""

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_alt = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    def image_tag(self):
        if self.image:
            if self.image.url is not None:
                return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
            else:
                return ""
        else:
            return ""


VARIANTS = (('None', 'None'),
            ('Size', 'Size'),
            ('Color', 'Color'),
            ('Size-Color', 'Size-Color'),
            )


class Product(models.Model):
    """Model for product information"""

    class Meta:
        verbose_name_plural = 'Products'

    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.CASCADE)
    slug = models.SlugField(null=True, default=None, unique=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_alt = models.CharField(max_length=254, null=True, blank=True)
    variant_options = models.CharField(max_length=15, choices=VARIANTS,
                                       default='Size-Color')
    wishlist = models.ManyToManyField(User, related_name="wishlist",
                                      blank=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image:
            if self.image.url is not None:
                return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
            else:
                return ""
        else:
            return ""

    """ From https://github.com/dev-rathankumar/greatkart-pre-deploy/blob"""
    def averageReview(self):
        reviews = ProductReview.objects.filter(product=self).aggregate(average=Avg('review_rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ProductReview.objects.filter(product=self).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class Color(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color</p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class ImageVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    image_variant_alt = models.CharField(max_length=50, blank=True)
    image_variant = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image_variant:
            if self.image_variant.url is not None:
                return mark_safe('<img src="{}" height="50"/>'.format(self.image_variant.url))
            else:
                return ""
        else:
            return ""


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True,
                              blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True,
                             blank=True)
    image = models.ForeignKey(ImageVariant, on_delete=models.CASCADE,
                              null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    amount_in_stock = models.IntegerField()
    sale = models.BooleanField(default=False)
    discounted_price = models.DecimalField(
        max_digits=6, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return self.product.name


""" Adapted from Code Artisan Lab eCommerce demo """


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.IntegerField(
                    default=5, validators=[MinValueValidator(1),
                                           MaxValueValidator(5)]
    )

    class Meta:
        verbose_name_plural = 'Reviews'

    def get_review_rating(self):
        return self.review_rating
