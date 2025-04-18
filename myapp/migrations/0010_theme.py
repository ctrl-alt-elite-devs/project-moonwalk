# Generated by Django 5.1.7 on 2025-04-15 01:52

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0009_order_pre_tax_total_order_tax_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="Theme",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("backgroundColor", models.CharField(max_length=7)),
                ("dropDate", models.DateField(auto_now=True)),
                (
                    "bannerImg00",
                    models.ImageField(
                        storage=storages.backends.s3.S3Storage(),
                        upload_to="theme_img00/",
                    ),
                ),
                (
                    "bannerImg01",
                    models.ImageField(
                        storage=storages.backends.s3.S3Storage(),
                        upload_to="theme_img01/",
                    ),
                ),
                (
                    "bannerImg02",
                    models.ImageField(
                        storage=storages.backends.s3.S3Storage(),
                        upload_to="theme_img02/",
                    ),
                ),
                ("fontStyle", models.CharField(max_length=100)),
                ("dropTitle", models.CharField(max_length=30)),
                ("fontColor", models.CharField(max_length=7)),
                ("fontWeight", models.CharField(max_length=6)),
                (
                    "fontBorderThickness",
                    models.DecimalField(decimal_places=2, default=0, max_digits=3),
                ),
                ("borderColor", models.CharField(max_length=7)),
            ],
        ),
    ]
