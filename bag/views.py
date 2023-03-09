from django.shortcuts import render


def view_bag(request):
    ''' View to display contents of shopping bag '''

    return render(request, 'bag/bag.html')
