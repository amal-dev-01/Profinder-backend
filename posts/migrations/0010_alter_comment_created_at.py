# Generated by Django 4.2.9 on 2024-02-07 11:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0009_alter_comment_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 7, 17, 21, 45, 810670)
            ),
        ),
    ]
