# Generated by Django 3.1.2 on 2021-04-23 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout_monitor', '0002_auto_20210423_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewdetail',
            name='review_date',
            field=models.DateField(null=True),
        ),
    ]