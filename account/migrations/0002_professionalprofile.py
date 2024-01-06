# Generated by Django 5.0 on 2023-12-26 12:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfessionalProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("job", models.CharField(max_length=100, null=True)),
                ("experience", models.IntegerField(null=True)),
                ("skills", models.TextField(null=True)),
                (
                    "image",
                    models.ImageField(
                        default="default.jpg", null=True, upload_to="profile_pics"
                    ),
                ),
                ("bio", models.CharField(max_length=50, null=True)),
                ("address", models.CharField(max_length=100, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="professionalprofile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
