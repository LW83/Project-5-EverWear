# Generated by Django 3.2.18 on 2023-04-11 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20230407_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.imagevariant'),
        ),
    ]
