# Generated by Django 4.2.6 on 2024-06-24 10:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item_manager', '0011_remove_size_subcategory_size_subcategory'),
        ('shop', '0004_alter_item_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.RemoveField(
            model_name='item',
            name='size',
        ),
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='item_manager.size'),
        ),
    ]
