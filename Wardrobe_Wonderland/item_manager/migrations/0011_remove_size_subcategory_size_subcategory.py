# Generated by Django 4.2.6 on 2024-06-24 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item_manager', '0010_remove_size_subcategory_size_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='size',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='size',
            name='subcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='item_manager.subcategory'),
        ),
    ]
