# Generated by Django 4.2.3 on 2023-07-29 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=30)),
                ('category', models.CharField(choices=[('D', 'Dry'), ('W', 'Wet'), ('S', 'Snack')], max_length=1)),
                ('price', models.IntegerField()),
                ('unit', models.CharField(choices=[('g', 'g'), ('l', 'ml')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('race', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=0)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PetFeeder.food')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PetFeeder.pet')),
            ],
        ),
    ]