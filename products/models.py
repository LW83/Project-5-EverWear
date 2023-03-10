from django.db import models


class Category(models.Model):
    ''' Model for product categories'''

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


COLOUR = ((0, "EverWear Grey"), (1, "Black"), (2, "White"),
          (3, "EverWear Beige"), (4, "EverWear Green"),
          (5, "EverWear Navy"), (6, "EverWear Blue"))

SIZE = ((0, "Universal"), (1, "X-Small"), (2, "Small"),
        (3, "Medium"), (4, "Large"), (5, "X-Large"))


class Product(models.Model):
    '''Model for product information'''

    class Meta:
        verbose_name_plural = 'Products'

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    size = models.IntegerField(choices=SIZE)
    colour = models.IntegerField(choices=COLOUR)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    """ Stock and sale code leveraged from DNL Bowers """
    stock = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    sale = models.BooleanField(default=False)
    discounted_price = models.DecimalField(
        max_digits=6, decimal_places=0, null=True, blank=False)
    rating = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


# class ProductVariant(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     colour = models.ForeignKey(Colour,on_delete=models.CASCADE)
#     size = models.ForeignKey(Size, on_delete=models.CASCADE)
#     amount_in_stock = models.IntegerField()

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['product', 'color', 'size'],
#                 name='unique_prod_color_size_combo'
#             )
#         ]