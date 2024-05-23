# Generated by Django 4.2.7 on 2024-01-22 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_item_men_sub_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='size_dresses',
            field=models.CharField(blank=True, choices=[('XS', 'XS (US 2 / UK 4 / Europe 32)'), ('S', 'S (US 4 / UK 6 / Europe 34)'), ('M', 'M (US 6 / UK 8 / Europe 36)'), ('L', 'L (US 8 / UK 10 / Europe 38)'), ('XL', 'XL (US 10 / UK 12 / Europe 40)')], max_length=40, null=True),
        ),
    ]