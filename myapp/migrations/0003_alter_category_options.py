# Generated by Django 5.1.2 on 2024-11-18 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_cart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]