# Generated by Django 2.2.4 on 2021-01-28 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_auto_20210128_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merch',
            name='size',
            field=models.CharField(default='small', max_length=255),
        ),
    ]