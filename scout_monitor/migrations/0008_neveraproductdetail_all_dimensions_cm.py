# Generated by Django 3.1.2 on 2021-06-25 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout_monitor', '0007_auto_20210625_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='neveraproductdetail',
            name='all_dimensions_cm',
            field=models.CharField(default='NO DATA', max_length=500),
        ),
    ]
