# Generated by Django 4.2.9 on 2024-01-18 08:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adminpanel", "0006_alter_payment_stripe_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="is_completed",
            field=models.BooleanField(default=False),
        ),
    ]
