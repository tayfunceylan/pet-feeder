# Generated by Django 4.2.4 on 2023-09-07 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_food_pl"),
    ]

    operations = [
        migrations.AlterField(
            model_name="food",
            name="price",
            field=models.FloatField(),
        ),
    ]
