# Generated by Django 4.1.7 on 2023-04-20 10:14

import collections
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('delivery_cost', models.FloatField(blank=True)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SizeChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eu_sizes', jsonfield.fields.JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})),
                ('us_sizes', jsonfield.fields.JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})),
                ('uk_sizes', jsonfield.fields.JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})),
                ('cm_sizes', jsonfield.fields.JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.category')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.gender')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('price', models.FloatField()),
                ('size', models.FloatField(blank=True)),
                ('link', models.URLField(max_length=1000)),
                ('attributes', models.ManyToManyField(to='main_app.attributevalue')),
                ('brands', models.ManyToManyField(to='main_app.brand')),
                ('category', models.ManyToManyField(to='main_app.category')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.gender')),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.website')),
            ],
        ),
    ]
