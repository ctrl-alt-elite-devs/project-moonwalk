# Generated by Django 5.1.7 on 2025-04-21 21:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_alter_theme_dropdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='unsubscribe_token',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
