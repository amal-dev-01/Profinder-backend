# Generated by Django 5.0 on 2024-01-05 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
