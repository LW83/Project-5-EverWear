# Generated by Django 3.2.18 on 2023-03-22 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20230322_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colour',
            old_name='colour',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='size',
            old_name='size',
            new_name='name',
        ),
    ]