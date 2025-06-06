# Generated by Django 5.1.2 on 2025-01-11 08:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_orderitem_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatus',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='latest_status', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('On Route', 'On Route'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], max_length=50),
        ),
    ]
