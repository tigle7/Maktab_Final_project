# Generated by Django 3.2.10 on 2022-01-20 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_remove_product_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
