# Generated by Django 4.2.6 on 2024-06-27 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_userorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='status',
            field=models.CharField(choices=[('Received', 'Received'), ('Scheduled', 'Scheduled'), ('Shipped', 'Shipped'), ('In Progress', 'In Progress')], default='In Progress', max_length=100),
        ),
    ]
