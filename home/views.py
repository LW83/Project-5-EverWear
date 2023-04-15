from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages

from products.models import Category


def landing_page(request):
    """ View to display landing page of site """

    return render(request, 'home/landing_page.html')


def index(request):
    """ View to display index page """

    return render(request, 'home/index.html')


def about(request):
    """ View to display about us page of site """

    return render(request, 'home/about.html')


def shipping(request):
    """ View to display shipping page of site """

    return render(request, 'home/shipping.html')


def privacy(request):
    """ View to display privacy page of site """

    return render(request, 'home/privacy.html')


def all_categories(request):
    """ Get all categories for display of cards on homepage """

    categories = Category.objects.all()
    paginate_by = 9

    context = {
        'categories': categories,
    }

    return render(request, 'home/index.html', context)
