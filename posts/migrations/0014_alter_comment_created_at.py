# Generated by Django 4.2.9 on 2024-02-07 12:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0013_alter_comment_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 7, 18, 18, 28, 763139)
            ),
        ),
    ]