# Generated by Django 4.0 on 2021-12-30 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_shop_proucts_alter_product_category_shoptype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='type',
        ),
        migrations.AlterField(
            model_name='shop',
            name='proucts',
            field=models.ManyToManyField(related_name='products', to='shop.Product'),
        ),
    ]