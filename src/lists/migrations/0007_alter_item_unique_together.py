# Generated by Django 5.0.7 on 2024-07-23 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0006_item_list"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="item",
            unique_together={("list", "text")},
        ),
    ]
