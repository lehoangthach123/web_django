# Generated by Django 4.1.7 on 2023-05-01 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='descriptions',
            field=models.TextField(default=None),
        ),
    ]
