# Generated by Django 4.1.7 on 2023-04-20 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attributevalue',
            name='name',
        ),
        migrations.RemoveField(
            model_name='sizechart',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='sizechart',
            name='category',
        ),
        migrations.RemoveField(
            model_name='sizechart',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='product',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='AttributeValue',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Gender',
        ),
        migrations.DeleteModel(
            name='SizeChart',
        ),
    ]
