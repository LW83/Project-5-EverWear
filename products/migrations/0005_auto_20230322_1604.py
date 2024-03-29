# Generated by Django 3.2.18 on 2023-03-22 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour', models.CharField(max_length=30)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=30)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='colour',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='image_alt',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='variant',
            field=models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Colour', 'Colour'), ('Size-Colour', 'Size-Colour')], default='Size-Colour', max_length=15),
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_stock', models.BooleanField(default=True)),
                ('amount_in_stock', models.IntegerField()),
                ('discounted_price', models.DecimalField(decimal_places=0, max_digits=6, null=True)),
                ('image_id', models.IntegerField(blank=True, default=0, null=True)),
                ('colour', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.colour')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.size')),
            ],
        ),
        migrations.CreateModel(
            name='ImageVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt', models.CharField(blank=True, max_length=50)),
                ('image_variant', models.ImageField(blank=True, null=True, upload_to='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_variant', to='products.product')),
            ],
        ),
    ]
