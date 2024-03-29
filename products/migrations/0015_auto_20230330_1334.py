# Generated by Django 3.2.18 on 2023-03-30 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_productreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_stock', models.BooleanField(default=True)),
                ('amount_in_stock', models.IntegerField()),
                ('sale', models.BooleanField(default=False)),
                ('discounted_price', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True)),
                ('colour', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.colour')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.imagevariant')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.DeleteModel(
            name='Variant',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.size'),
        ),
    ]
