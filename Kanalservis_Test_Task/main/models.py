# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class OrderbookModel(models.Model):
    # python manage.py inspectdb orderbook > main/models.py
    orderbook_id = models.IntegerField(blank=True, null=True)
    ordernumber = models.IntegerField(primary_key=True)
    price = models.IntegerField(blank=True, null=True)
    deliverytime = models.DateField(blank=True, null=True)
    price_rub = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orderbook'
