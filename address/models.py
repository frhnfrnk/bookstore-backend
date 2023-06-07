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