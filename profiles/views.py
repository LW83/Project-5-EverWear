from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order
from products.models import Product


@login_required
def profile(request):
    """ Display the user's profile """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update error. Form updates are invalid.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """ Display user's order history"""
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is confirmation of previous order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def wishlist(request):
    """ Display user's wishlist items from Very Academy Tutorial """
    products = Product.objects.filter(wishlist=request.user)
    return render(request, "profiles/profile/wishlist.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.wishlist.filter(id=request.user.id).exists():
        product.wishlist.remove(request.user)
        messages.success(request, f'{product.name} has been removed from your Wishlist')
    else:
        product.wishlist.add(request.user)
        messages.success(request, f'Added {product.name} to your Wishlist')
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
