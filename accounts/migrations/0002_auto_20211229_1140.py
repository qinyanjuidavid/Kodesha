# Generated by Django 3.2.9 on 2021-12-29 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Client',
            new_name='Buyer',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Administrator', 'Administrator'), ('Buyer', 'Buyer'), ('Seller', 'Seller')], max_length=17, verbose_name='Role'),
        ),
    ]