# Generated by Django 3.2.18 on 2023-03-20 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='default_delivery_name',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='default_email',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]