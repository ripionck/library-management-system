# Generated by Django 5.0 on 2024-01-01 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='is_borrowed',
        ),
    ]
