# Generated by Django 2.2.8 on 2019-12-26 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(default='anonymous', max_length=30)),
                ('location', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='property')),
                ('price', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name_plural': 'house',
            },
        ),
        migrations.CreateModel(
            name='Interesting_house',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.House')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_date', models.DateTimeField(auto_now_add=True)),
                ('date_added', models.DateTimeField()),
                ('houses', models.ManyToManyField(to='myapp.Interesting_house')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Dashboard',
            },
        ),
    ]
