# Generated by Django 4.2.6 on 2024-06-24 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_manager', '0011_remove_size_subcategory_size_subcategory'),
        ('shop', '0005_alter_item_discount_remove_item_size_item_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='color',
            field=models.ManyToManyField(related_name='colors', to='item_manager.color'),
        ),
    ]
