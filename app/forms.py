from django import forms
from django import forms
from .models import *


class CreateOrderForm(forms.ModelForm):
    sender_address = forms.CharField(max_length=100, required=True)
    sender_name = forms.CharField(max_length=100, required=True)
    sender_contact = forms.CharField(max_length=100, required=True)
    receiver_address = forms.CharField(max_length=100, required=True)
    receiver_name = forms.CharField(max_length=100, required=True)
    receiver_contact = forms.CharField(max_length=100, required=True)
    payment_type = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Order
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update(
            {'class': 'form-control mb-3', })
        self.fields['shipping_fee'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Shipping Fee'})
        self.fields['sender_address'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Deliver From'})
        self.fields['sender_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Deliver From'})
        self.fields['sender_contact'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Deliver From', })
        self.fields['receiver_address'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Deliver To'})
        self.fields['receiver_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Deliver To'})
        self.fields['receiver_contact'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Deliver To'})
        self.fields['payment_type'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Payment method used'})


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update(
            {'class': 'form-control mb-3', })
        self.fields['seller_sku'].widget.attrs.update(
            {'class': 'form-control mb-3', })
        self.fields['shop_sku'].widget.attrs.update(
            {'class': 'form-control mb-3', })
        self.fields['price'].widget.attrs.update(
            {'class': 'form-control mb-3', })
        self.fields['quantity'].widget.attrs.update(
            {'class': 'form-control mb-3', })
        self.fields['product_name'].required = True
        self.fields['seller_sku'].required = True
        self.fields['shop_sku'].required = True
        self.fields['price'].required = True
        self.fields['quantity'].required = True


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = ReceiptDetails
        fields = ('order_status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_status'].widget.attrs.update(
            {'class': 'form-control mb-3 pb-1', })
