# Generated by Django 5.1.4 on 2025-01-06 18:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Product name')),
                ('description', models.TextField(verbose_name='Product description')),
                ('description_HTML', models.CharField(max_length=30, verbose_name='Product description HTML file')),
                ('qty_in_stock', models.IntegerField(verbose_name='In stock')),
                ('qty_reserved', models.IntegerField(verbose_name='In stock reserved')),
                ('qty_ordered', models.IntegerField(verbose_name='Ordered')),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Buy price')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.entity', verbose_name='Vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Packaging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Length in cm')),
                ('width', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Width in cm')),
                ('height', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Height in cm')),
                ('volume', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Volume in litres')),
                ('net_weight', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Net weight in kg')),
                ('gross_weight', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Gross weight in kg')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Product')),
            ],
        ),
    ]
