# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-13 22:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def fill_product_type_from_backup(apps, schema_editor):
    SubscriptionType = apps.get_model("subscriptions", "SubscriptionType")
    CustomerGroupTransform = apps.get_model("crm", "CustomerGroupTransform")
    Price = apps.get_model("crm", "Price")
    ProductPrice = apps.get_model("crm", "ProductPrice")
    UnitTransform = apps.get_model("crm", "UnitTransform")
    db_alias = schema_editor.connection.alias
    all_positions = Position.objects.using(db_alias).all()
    for position in all_positions:
        position.product_type = position.product_backup
        position.save()
    all_customer_group_transforms = CustomerGroupTransform.objects.using(db_alias).all()
    for customer_group_transform in all_customer_group_transforms:
        customer_group_transform.product_type = customer_group_transform.product_backup
        customer_group_transform.save()
    all_prices = Price.objects.using(db_alias).all()
    for price in all_prices:
        new_product_price = ProductPrice.objects.using(db_alias).create(price_ptr=price.id,
                                                                        product_type=price.product_backup)
        new_product_price.save()
    all_unit_transforms = UnitTransform.objects.using(db_alias).all()
    for unit_transform in all_unit_transforms:
        unit_transform.product_type = unit_transform.product_backup
        unit_transform.save()


def reverse_func(apps, schema_editor):
    return 1


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0048_auto_20181012_2056'),
        ('subscriptions', '0004_auto_20181013_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiontype',
            name='product_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.ProductType', verbose_name='Product Type'),
        ),
        migrations.RunPython(fill_product_type_from_backup, reverse_func),

    ]
