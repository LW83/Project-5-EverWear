from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages

from products.models import Category


def landing_page(request):
    """ View to display landing page of site """

    return render(request, 'home/landing_page.html')


def index(request):
    ''' View to display index page '''

    return render(request, 'home/index.html')


def all_categories(request):

    categories = Category.objects.all()
    paginate_by = 9

    context = {
        'categories': categories,
    }

    return render(request, 'home/index.html', context)
