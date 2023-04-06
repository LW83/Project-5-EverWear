from django.shortcuts import (get_object_or_404, HttpResponse, render,
                              redirect, reverse)
from django.contrib import messages
from products.models import Product, ProductAttribute


def view_bag(request):
    """ View to display contents of shopping bag """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add specified quantity of the specified product to the shopping bag """

    # product = Product.objects.get(pk=item_id)
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'size-box' in request.POST:
        print('SIZE IS WORKING')
        size = request.POST['size-box']
    color = None
    if 'color-box' in request.POST:
        print('COLOR IS WORKING')
        color = request.POST['color-box']

    print('SIZE: ', size)
    print('COLOR: ', color)
    bag = request.session.get('bag', {})

    if size and color:
        if item_id in list(bag.keys()):
            if size and color in bag[item_id]['items_by_size']['items_by_color'].keys():
                bag[item_id]['item_by_size'][size]['items_by_color'][color] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} in {color.name} quantity to {bag[item_id]["items_by_size"][size]["items_by_color"][color]}')
            else:
                bag[item_id]['size'][size] = quantity
                messages.success(request, f'Added {product.name} in size {size.upper()} to your bag')
        else:
            bag[item_id] = {'size': {size: quantity}}
            messages.success(request, f'Added {product.name} in size {size.upper()} to your bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'{product.name} has been added to your bag')

    request.session['bag'] = bag
    print(bag)
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed {product.name} in size {size.upper()} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed {product.name} in size {size.upper()} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
