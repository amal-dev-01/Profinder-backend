# Generated by Django 4.2.9 on 2024-02-08 05:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0021_message_sender"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="sender",
        ),
    ]