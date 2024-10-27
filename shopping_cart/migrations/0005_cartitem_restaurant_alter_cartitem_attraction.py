# Generated by Django 5.1.2 on 2024-10-27 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_auto_20241025_0234'),
        ('shopping_cart', '0004_remove_cart_booking_id'),
        ('tourist_attraction', '0005_auto_20241023_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='attraction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tourist_attraction.touristattraction'),
        ),
    ]