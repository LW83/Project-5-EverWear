# Generated by Django 3.2.18 on 2023-03-30 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20230330_1334'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Colour',
            new_name='Color',
        ),
        migrations.RenameField(
            model_name='productattribute',
            old_name='colour',
            new_name='color',
        ),
        migrations.AlterField(
            model_name='product',
            name='variant_options',
            field=models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Size-Color', 'Size-Color')], default='Size-Color', max_length=15),
        ),
    ]