# Generated by Django 4.2.6 on 2024-04-29 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_orderitem_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='paid',
        ),
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
