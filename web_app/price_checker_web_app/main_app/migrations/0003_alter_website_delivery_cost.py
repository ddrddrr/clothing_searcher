# Generated by Django 4.1.7 on 2023-04-20 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_attributevalue_name_remove_sizechart_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='delivery_cost',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
