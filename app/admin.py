from django.contrib import admin
from .models import *


class OrderDisplay(admin.ModelAdmin):
    list_display = ('id', 'price', 'quantity',
                    'subtotal', 'shipping_fee', 'total')


admin.site.register(Product)
admin.site.register(Order, OrderDisplay)
admin.site.register(Sender)
admin.site.register(Receiver)
admin.site.register(ReceiptDetails)
