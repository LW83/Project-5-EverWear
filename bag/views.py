from django.shortcuts import (get_object_or_404, HttpResponse, render,
                              redirect, reverse)
from django.contrib import messages
from products.models import Product, ProductAttribute


def view_bag(request):
    """ View to display contents of shopping bag """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add specified quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    item = None
    if 'size-box' and 'color-box' in request.POST:
        size = request.POST['size-box']
        color = request.POST['color-box']
        item = f'{item_id}_{size}_{color}'
    bag = request.session.get('bag', {})

    if item:
        if item_id in list(bag.keys()):
            if item in bag[item_id]['items_by_variation'].keys():
                bag[item_id]['items_by_variation'][item] += quantity
                messages.success(
                    request, f'Updated {product.name} '
                    f'size {size.upper()} quantity in {color} to '
                    f'{bag[item_id]["items_by_variation"][item]}'
                    )
            else:
                bag[item_id]['items_by_variation'][item] = quantity
                messages.success(
                    request,
                    f'Added {product.name} '
                    f'size {size.upper()} in {color} to your bag'
                    )
        else:
            bag[item_id] = {'items_by_variation': {item: quantity}}
            messages.success(
                request,
                f'Added {product.name} '
                f'size {size.upper()} in {color} to your bag'
                )
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(
                request,
                f'Updated {product.name} quantity to {bag[item_id]}'
                )
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    print(bag)
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    item = None
    if 'product_item' in request.POST:
        size = request.POST['size-box']
        color = request.POST['color-box']
        item = f'{item_id}_{size}_{color}'
    bag = request.session.get('bag', {})

    if item:
        if quantity > 0:
            bag[item_id]['items_by_variation'][item] = quantity
            messages.success(
                request, f'Updated {product.name} '
                f'size {size.upper()} in '
                f'color {color} quantity to '
                f'{bag[item_id]["items_by_variation"][item]}'
                )
        else:
            del bag[item_id]['items_by_variation'][item]
            if not bag[item_id]['items_by_variation']:
                bag.pop(item_id)
            messages.success(
                request,
                f'Removed {product.name} '
                f'size {size.upper()} in '
                f'{color} from your bag'
                )
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(
                request,
                f'Updated {product.name} quantity to {bag[item_id]}'
                )
        else:
            bag.pop(item_id)
            messages.success(
                request,
                f'Removed {product.name} from your bag'
                )

    request.session['bag'] = bag
    return redirect(reverse(view_bag))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        item = None
        if 'size-box' and 'color-box' in request.POST:
            size = request.POST['size-box']
            color = request.POST['color-box']
            item = f'{item_id}_{size}_{color}'
        bag = request.session.get('bag', {})

        if item:
            del bag[item_id]['items_by_variation'][item]
            if not bag[item_id]['items_by_variation']:
                bag.pop(item_id)
            messages.success(
                request,
                f'Removed 'f'{product.name} in {size.upper()} and {color} from your bag'
                )
        else:
            if item_id in list(bag.keys()):
                bag.pop(item_id)
                messages.success(
                    request,
                    f'Removed {product.name} from your bag'
                    )

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        print(e)
        return HttpResponse(status=500)
