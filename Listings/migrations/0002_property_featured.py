# Generated by Django 3.2.9 on 2022-01-03 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='featured'),
        ),
    ]