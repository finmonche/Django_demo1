# Generated by Django 4.1.4 on 2023-01-01 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('birthday', models.DateField(null=True)),
            ],
            options={
                'db_table': 'Customers',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('description', models.CharField(max_length=200, null=True)),
                ('brand', models.CharField(max_length=30, null=True)),
                ('cpu_brand', models.CharField(max_length=30, null=True)),
                ('cpu_type', models.CharField(max_length=30, null=True)),
                ('memory_capacity', models.CharField(max_length=30, null=True)),
                ('hd_capacity', models.CharField(max_length=30, null=True)),
                ('card_model', models.CharField(max_length=30, null=True)),
                ('displaysize', models.CharField(max_length=30, null=True)),
                ('image', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'Goods',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField()),
                ('status', models.IntegerField(default=1)),
                ('total', models.FloatField()),
            ],
            options={
                'db_table': 'Orders',
                'ordering': ['order_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('sub_total', models.FloatField(default=0.0)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.goods')),
                ('orders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.orders')),
            ],
            options={
                'db_table': 'OrderLineItems',
                'ordering': ['id'],
            },
        ),
    ]
