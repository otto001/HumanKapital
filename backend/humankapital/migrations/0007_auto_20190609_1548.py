# Generated by Django 2.1.4 on 2019-06-09 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humankapital', '0006_auto_20190609_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='karma',
            field=models.FloatField(default=1),
        ),
    ]
