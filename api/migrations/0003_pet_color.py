# Generated by Django 4.2.3 on 2023-08-12 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_meal_pet_meal_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]