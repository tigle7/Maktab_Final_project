# Generated by Django 3.2.10 on 2022-01-06 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_product_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True),
        ),
    ]
