# Generated by Django 3.2.18 on 2023-03-22 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20230322_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='discounted_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True),
        ),
    ]