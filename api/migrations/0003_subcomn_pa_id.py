# Generated by Django 4.0.3 on 2022-05-12 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcomn',
            name='pa_id',
            field=models.BigIntegerField(default=0),
        ),
    ]