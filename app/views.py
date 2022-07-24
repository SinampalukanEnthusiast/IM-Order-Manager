from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Count, Q, Sum, Avg
from django.db import connection


def index(request):
    context = {}
    return render(request, 'index.html', context)


def orders(request):
    orders = Order.objects.all()
    seller_sku_get = request.GET.get('seller_sku')
    shop_sku = request.GET.get('shop_sku')
    order_id_filter = request.GET.getlist('order_id_filter')
    order_id_filter = [int(i) for i in order_id_filter]
    having = request.GET.get('having')
    orders_total = Order.objects.all().count()
    products_total = Product.objects.all().count()
    products_inventory_value = Product.objects.all().aggregate(price__avg=Avg('price'))
    order_status_filter = None

    try:
        max_price = int(request.GET.get('max_price'))
    except:
        max_price = None

    try:
        min_price = int(request.GET.get('min_price'))
    except:
        min_price = None
    order_status = request.GET.get('order_status')
    if seller_sku_get != '' and seller_sku_get is not None:
        orders = orders.filter(product__seller_sku=seller_sku_get)
    elif shop_sku != '' and shop_sku is not None:
        orders = orders.filter(product__shop_sku=shop_sku)

    elif min_price is not None and max_price is not None:
        orders = orders.filter(product__price__gte=min_price,
                               product__price__lte=max_price)

    elif max_price is not None:
        orders = orders.filter(product__price__lte=max_price)
    elif min_price is not None:
        orders = orders.filter(product__price__gte=min_price)
    elif order_status != '' and order_status is not None:
        orders = orders.filter(receiptdetails__order_status=order_status)
        order_status_filter = Order.objects.values(
            'receiptdetails__order_status').filter(receiptdetails__order_status=order_status).annotate(count_with_filter=Count('id'))
        for i in order_status_filter:
            if i['count_with_filter']:
                order_status_filter = i['count_with_filter']

    elif order_id_filter:
        orders = Order.objects.filter(id__in=order_id_filter)
    elif having is not None:
        orders_having = Order.objects.values('product__shop_sku').annotate(
            avg=Avg('product__price')).filter(avg__gte=having)
        orders_having_shop_sku = []
        for i in orders_having:
            if i['product__shop_sku']:
                orders_having_shop_sku.append(i['product__shop_sku'])
        orders = orders.filter(
            product__shop_sku__in=orders_having_shop_sku).order_by('-product__price')

    products = Product.objects.filter(
        order__id__in=orders).values('order__id', 'product_name')

    context = {'orders': orders, 'products': products,
               'total_orders': orders_total, 'products_total': products_total, 'products_inventory_value': products_inventory_value, 'order_status_filter': order_status_filter}

    return render(request, 'orders.html', context)


def create_order(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['sender_name']
            sender_address = form.cleaned_data['sender_address']
            sender_contact = form.cleaned_data['sender_contact']
            receiver_name = form.cleaned_data['receiver_name']
            receiver_address = form.cleaned_data['receiver_address']
            receiver_contact = form.cleaned_data['receiver_contact']
            payment_type = form.cleaned_data['payment_type']

            order_id = form.save()
            sender = Sender.objects.create(
                sender_address=sender_address, sender_name=sender_name, sender_contact=sender_contact)
            receiver = Receiver.objects.create(
                receiver_name=receiver_name, receiver_address=receiver_address, receiver_contact=receiver_contact,)
            receipt = ReceiptDetails.objects.create(
                order_fk=order_id, sender_fk=sender, receiver_fk=receiver, order_status='Processing',  payment_type=payment_type)
            messages.success(
                request, 'Order Created Successfully!')
    else:
        form = CreateOrderForm()
    context = {'products': products, 'form': form}
    return render(request, 'create_order.html', context)


def add_product(request):
    if request.method == "POST":
        form = CreateProductForm(request.POST)
        if form.is_valid():
            form.save()
        messages.success(
            request, 'Product Created Successfully!')
    else:
        form = CreateProductForm()
    context = {'form': form}
    return render(request, 'add_product.html', context)


def order_delete(request, id):
    order = Order.objects.get(id=id).delete()
    messages.success(request, 'Order successfully deleted!')
    return redirect('orders')


def order_detail(request, id):
    order = Order.objects.get(id=id)
    values = Order.objects.filter(id=id).values('shipping_fee',
                                                'product__price', 'product__quantity',)
    if request.method == "POST":
        form = UpdateStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['order_status']
            receipt = ReceiptDetails.objects.filter(
                order_fk=order).update(order_status=status)

    else:
        form = UpdateStatusForm()
    context = {'order': order, 'form': form}
    return render(request, 'order_detail.html', context)
