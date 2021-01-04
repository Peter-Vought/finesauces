from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from listings.models import Product
from .forms import CartAddProductForm
from decimal import Decimal

def get_cart(request):
    cart = request.session.get(settings.CART_ID)
    if not cart:
        cart = request.session[settings.CART_ID] = {}
    return cart

def cart_add(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    product_id = str(product.id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data

        if product_id not in cart:
            cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if request.POST.get('overwrite_qty'):
            cart[product_id]['quantity'] = cd['quantity']
        else:
            cart[product_id]['quantity'] += cd['quantity']

        request.session.modified = True

        return redirect('cart:cart_detail')

def cart_detail(request):
    cart = get_cart(request)
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    temp_cart = cart.copy()

    for product in products:
        cart_item = temp_cart[str(product.id)]
        cart_item['product'] = product
        cart_item['total_price'] = (Decimal(cart_item['price'])
                                    * cart_item['quantity'])
        cart_item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': cart_item['quantity']
        })

    cart_total_price = sum(Decimal(item['price']) * item['quantity'] 
                        for item in temp_cart.values())

    return render(
        request,
        'detail.html',
        {
            'cart': temp_cart.values(),
            'cart_total_price': cart_total_price
        })

def cart_remove(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]

        request.session.modified = True

        return redirect('cart:cart_detail')

def cart_clear(request):
    del request.session[settings.CART_ID]
