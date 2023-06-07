from django.db import models
from store.models import Inventory
from customer.models import Customer
from staff.models import Staff

# Create your models here.

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING)
    staff = models.ForeignKey(Staff, models.DO_NOTHING)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    order_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order'

class OrderHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order_history'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING)
    staff = models.ForeignKey(Staff, models.DO_NOTHING)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment'
