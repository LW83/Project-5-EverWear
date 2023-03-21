from django.shortcuts import render


def landing_page(request):
    """ View to display landing page of site """

    return render(request, 'home/landing_page.html')


def index(request):
    ''' View to display index page '''

    return render(request, 'home/index.html')
