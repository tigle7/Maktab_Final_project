# Generated by Django 4.0 on 2021-12-29 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_cart_cartitem_cart_items_cart_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_active',
            new_name='is_available',
        ),
    ]
