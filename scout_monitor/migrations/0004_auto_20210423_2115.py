# Generated by Django 3.1.2 on 2021-04-23 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout_monitor', '0003_auto_20210423_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productprice',
            name='daily_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='productprice',
            name='normal_price',
            field=models.FloatField(default=0.0),
        ),
    ]