# Generated by Django 3.2.8 on 2021-10-30 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='profit',
            field=models.FloatField(default=0),
        ),
    ]