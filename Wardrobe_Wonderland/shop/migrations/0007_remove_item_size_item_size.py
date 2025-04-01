# Generated by Django 4.2.6 on 2024-06-24 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_manager', '0011_remove_size_subcategory_size_subcategory'),
        ('shop', '0006_alter_item_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='size',
        ),
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.ManyToManyField(related_name='sizes', to='item_manager.size'),
        ),
    ]
