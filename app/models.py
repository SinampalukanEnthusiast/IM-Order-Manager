from ast import Or
from tabnanny import verbose
from django.db import models

# Create your models here.


class Sender(models.Model):
    sender_address = models.CharField(
        max_length=150, verbose_name="Address", blank=True, null=True)
    sender_name = models.CharField(
        max_length=150, verbose_name="Full Name", blank=True, null=True)
    sender_contact = models.CharField(
        max_length=150, verbose_name="Contact No.", blank=True, null=True)

    def __str__(self):
        return self.sender_name


class Receiver(models.Model):
    receiver_address = models.CharField(
        max_length=150, verbose_name="Address", blank=True, null=True)
    receiver_name = models.CharField(
        max_length=150, verbose_name="Full Name", blank=True, null=True)
    receiver_contact = models.CharField(
        max_length=150, verbose_name="Contact No.", blank=True, null=True)

    def __str__(self):
        return self.receiver_name


class Product(models.Model):
    product_name = models.CharField(
        max_length=150, verbose_name="Product Name", blank=True, null=True)
    seller_sku = models.CharField(
        max_length=100, verbose_name="Seller SKU", blank=True, null=True)
    shop_sku = models.CharField(
        max_length=100, verbose_name="Shop SKU", blank=True, null=True)
    price = models.IntegerField(
        verbose_name="Product Price", blank=True, default=0, null=True)
    quantity = models.IntegerField(
        default=0, verbose_name="Quantity", blank=True, null=True)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shipping_fee = models.IntegerField(
        verbose_name="Order shipping_fee", blank=True, null=True)

    def __str__(self):
        return f'Order: {self.product.product_name} | Qty: {self.product.quantity} '

    @property
    def price(self):
        return self.product.price

    @property
    def quantity(self):
        return self.product.quantity

    @property
    def subtotal(self):
        return self.product.price * self.product.quantity

    @property
    def total(self):
        return self.subtotal + self.shipping_fee

    @property
    def status(self):
        return self.receiptdetails.order_status

    @property
    def sender(self):
        return self.receiptdetails.sender_fk

    @property
    def receiver(self):
        return self.receiptdetails.receiver_fk

    @property
    def receipt_print(self):
        return self.receiptdetails.print_date

    @property
    def payment_type(self):
        return self.receiptdetails.payment_type


class ReceiptDetails(models.Model):
    order_status_choices = (('Processing', 'Processing'),
                            ('To Pack', 'To Pack'),
                            ('Shipping', 'Shipping'),
                            ('Delivered', 'Delivered'),)
    order_fk = models.OneToOneField(
        Order, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Order Foreign Key")
    sender_fk = models.ForeignKey(
        Sender, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Sender Foreign Key")
    receiver_fk = models.ForeignKey(
        Receiver, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Receiver Foreign Key")

    order_status = models.CharField(
        choices=order_status_choices, max_length=50, blank=True, null=True, verbose_name="Order Status")
    print_date = models.DateField(
        auto_now_add=True, blank=True, null=True, verbose_name="Date Printed")
    payment_type = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Payment Type")

    def __str__(self):
        return f'{self.order_fk} - From {self.sender_fk} to {self.receiver_fk}'

    class Meta:
        verbose_name = 'Receipt Detail'
        verbose_name_plural = 'Receipt Details'
