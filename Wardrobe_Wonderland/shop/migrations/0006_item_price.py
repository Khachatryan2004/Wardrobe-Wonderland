# Generated by Django 4.2.7 on 2023-12-17 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_item_category_alter_item_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10000, max_digits=10),
            preserve_default=False,
        ),
    ]
