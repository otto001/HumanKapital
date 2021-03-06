# Generated by Django 2.1.4 on 2019-06-08 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humankapital', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acquisition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True)),
                ('percent', models.IntegerField()),
                ('price', models.IntegerField()),
                ('sold', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='alive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='acquisition',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acquired_by', to='humankapital.Person'),
        ),
        migrations.AddField(
            model_name='acquisition',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acquisitions', to=settings.AUTH_USER_MODEL),
        ),
    ]
