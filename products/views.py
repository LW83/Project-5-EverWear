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
from .forms import ProductForm, ReviewForm


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

    # product = get_object_or_404(Product, pk=product_id)
    # reviews = ProductReview.objects.filter(product_id=product.id)
    product = Product.objects.get(id=id)
    product_attributes = ProductAttribute.objects.filter(product=product)
    colors = ProductAttribute.objects.filter(product=product).values('color__id', 'color__name', 'color__code').distinct()
    sizes = ProductAttribute.objects.filter(product=product).values('size__id', 'size__name', 'size__code', 'color__id').distinct()
    reviewForm = ReviewForm()

    # canAdd = True
    # if request.user.is_authenticated:
    #     reviewCheck = ProductReview.objects.filter(user=request.user, product=product).count()
    #     if reviewCheck > 0:
    #         canAdd = False

    reviews = ProductReview.objects.filter(product=product)
    count_reviews = ProductReview.objects.filter(product=product).aggregate(count=Count('id'))
    # count = 0
    # if reviews['count'] is not None:
    #     count = int(reviews['count'])
    #     return count

    # avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))

    # def averageReview(self):
    #     reviews = ProductReview.objects.filter(product=self).aggregate(average=Avg('rating'))
    #     avg = 0
    #     if reviews['average'] is not None:
    #         avg = float(reviews['average'])
    #     return avg

    context = {
        'product': product,
        'reviewForm': reviewForm,
        'reviews': reviews,
        # 'canAdd': canAdd,
        'count_reviews': count_reviews,
        # 'avg_reviews': avg_reviews,
        'colors': colors,
        'sizes': sizes,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you do not have permission to add products.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product has been successfully added.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you do not have permission to edit products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Selected product has been successfully updated.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
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
        messages.error(request, 'Sorry, you do not have permission to delete products.')
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

    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))

    return JsonResponse({'bool': True, 'data': data, 'avg_reviews': avg_reviews})

# url = request.META.get('HTTP_REFERER')
    # if request.method == 'POST':
    #     try:
    #         reviews = ProductReview.objects.get(user__id=request.user.id, product__id=product_id)
    #         form = ReviewForm(request.POST, instance=reviews)
    #         form.save()
    #         messages.success(request, 'Thank you! Your review has been updated.')
    #         return redirect(reverse('product_detail', args=[product.id]))
    #     except ProductReview.DoesNotExist:
    #         form = ReviewForm(request.POST)
    #         if form.is_valid():
    #             data = ProductReview()
    #             data.review_rating = form.cleaned_data['review_rating']
    #             data.review_text = form.cleaned_data['review_text']
    #             data.product_id = product_id
    #             data.user_id = request.user.id
    #             data.save()
    #             messages.success(request, 'Thank you! Your review has been submitted.')
    #             return redirect(reverse('product_detail', args=[product.id]))
