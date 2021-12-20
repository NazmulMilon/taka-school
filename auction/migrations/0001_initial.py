# Generated by Django 3.2.8 on 2021-12-20 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashed_id', models.CharField(blank=True, db_index=True, max_length=16, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('price', models.FloatField()),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashed_id', models.CharField(blank=True, db_index=True, max_length=16, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ('description', models.TextField()),
                ('photo', models.ImageField(default='product/product.png', upload_to='product/%Y/%m/%d/')),
                ('min_bid_price', models.FloatField()),
                ('auction_end_date', models.DateTimeField()),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]