# Generated by Django 4.2.3 on 2023-09-21 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_specificatoin_product_specification'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_count',
            field=models.IntegerField(default='20'),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default='Product Type', max_length=100),
        ),
    ]
