# Generated by Django 5.1.7 on 2025-04-14 22:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_order_pre_tax_total_order_tax_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('banner_image', models.ImageField(upload_to='newsletter_banners/')),
                ('description', models.TextField()),
                ('store_link', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='subscriber',
            name='unsubscribe_token',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
    ]
