from django import forms
from .widgets import CustomClearableFileInput
from .models import (Product, Category, ProductReview, ProductAttribute,
                     Color, Size)


class CategoryForm(forms.ModelForm):
    """Form to allow editing of categories"""

    class Meta:
        model = Category
        fields = ('name', 'friendly_name', 'image',
                  'image_alt',)

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)


class ProductForm(forms.ModelForm):
    """Form to allow editing of products"""

    class Meta:
        model = Product
        fields = ('category', 'sku', 'name', 'description', 'price',
                  'image', 'image_alt', 'variant_options')

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-1'


class ProductVariationForm(forms.ModelForm):
    """Form to allow editing of products"""

    class Meta:
        model = ProductAttribute
        fields = ('__all__')

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['review_text', 'review_rating']
