from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Max, Min, Count, Avg
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .models import (Category, Product, ProductAttribute,
                     Color, Size, ImageVariant,
                     ProductReview)
from .forms import ProductForm, ReviewForm, ProductVariationForm, CategoryForm


def all_products(request):
    """ A view to show all products, sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    paginate_by = 9

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, id):
    """ A view to show individual product details """

    product = Product.objects.get(id=id)
    product_attributes = ProductAttribute.objects.filter(product=product)
    category = Category.objects.all()
    colors = ProductAttribute.objects.filter(product=product).values('color__id', 'color__name', 'color__code').distinct()
    sizes = ProductAttribute.objects.filter(product=product).values('size__id', 'size__name', 'size__code', 'color__id').distinct()
    reviewForm = ReviewForm()

    canAdd = True
    if request.user.is_authenticated:
        reviewCheck = ProductReview.objects.filter(user=request.user,
                                                   product=product).count()
        if reviewCheck > 0:
            canAdd = False

    reviews = ProductReview.objects.filter(product=product)

    context = {
        'product': product,
        'reviewForm': reviewForm,
        'reviews': reviews,
        'canAdd': canAdd,
        'category': category,
        'colors': colors,
        'sizes': sizes,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def manage_store(request):
    """ View to display manage store page """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you do not have permission to access.')
        return redirect(reverse('home'))
    else:
        return render(request, 'products/manage_store.html')


@login_required
def add_category(request):
    """ Add a category to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you do not have permission \
                                 to add cateogries.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Category has been successfully added.')
            return redirect(reverse('manage_store'))
        else:
            messages.error(request, 'Failed to add category. Please ensure \
                                    the form is valid.')
    else:
        form = CategoryForm()

    template = 'products/add_category.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you do not have permission to \
                                 add products.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product has been successfully added.')
            return redirect(reverse('manage_store'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the \
                                     form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_variation(request):
    """ Add a variation to the store - adapted from LadCode 2021"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductVariationForm(request.POST, request.FILES)
        if form.is_valid():
            product_variant = form.save()
            messages.success(request, 'Product variant has been successfully \
                                       added.')
            return redirect(reverse('manage_store'))
        else:
            messages.error(request, 'Failed to add product. Please ensure \
                                     the form is valid.')
    else:
        form = ProductVariationForm()

    template = 'products/add_variation.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you do not have permission to \
                                 edit products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Selected product has been successfully \
                                       updated.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure \
                                     the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you do not have permission to delete \
                                 products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product succesfully deleted.')
    return redirect(reverse('products'))


def submit_review(request, product_id):
    product = Product.objects.get(pk=product_id)
    user = request.user
    form = ReviewForm
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
        )
    data = {
        'user': user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }

    return JsonResponse({'bool': True, 'data': data})
