from django.db import models
from staff.models import Staff

# Create your models here.

class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'language'

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    publication_year = models.IntegerField()
    language = models.ForeignKey('Language', models.DO_NOTHING)
    num_pages = models.IntegerField()
    publisher = models.ForeignKey('Publisher', models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition_value = models.TextField()  # This field type is a guess.
    isbn13 = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'

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

class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    publisher_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'publisher'


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, models.DO_NOTHING)
    book = models.ForeignKey(Book, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventory'
