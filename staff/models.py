from django.db import models
# Create your models here.


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=50)
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=255)
    store = models.ForeignKey('Store', models.DO_NOTHING, related_name='+')
    address = models.ForeignKey(Address, models.DO_NOTHING)
    is_manager = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    address = models.ForeignKey(Address, models.DO_NOTHING)
    staff = models.ForeignKey(Staff, models.DO_NOTHING, related_name='+')
    store_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'store'
