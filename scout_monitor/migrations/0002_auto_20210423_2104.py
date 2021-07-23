# Generated by Django 3.1.2 on 2021-04-23 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scout_monitor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='total_qualification',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='reviewdetail',
            name='comment',
            field=models.TextField(default='No comment'),
        ),
        migrations.AlterField(
            model_name='reviewdetail',
            name='qualification',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='reviewdetail',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scout_monitor.productreview'),
        ),
    ]
