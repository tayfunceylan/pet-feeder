# Generated by Django 4.2.3 on 2023-09-24 23:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_schedule_food'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='weekdays',
            field=models.IntegerField(default=127, validators=[django.core.validators.MaxValueValidator(127)]),
        ),
    ]
