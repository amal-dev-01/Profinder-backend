# Generated by Django 4.2.9 on 2024-01-17 09:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adminpanel", "0003_payment_total_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="customer_id",
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="stripe_id",
            field=models.CharField(blank=True, null=True),
        ),
    ]
