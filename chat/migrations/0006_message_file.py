# Generated by Django 5.0 on 2024-01-11 12:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0005_rename_content_message_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="uploads/"),
        ),
    ]