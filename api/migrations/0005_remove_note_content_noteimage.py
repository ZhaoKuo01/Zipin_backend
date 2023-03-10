# Generated by Django 4.0.3 on 2022-05-16 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_mylike_mycollection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='content',
        ),
        migrations.CreateModel(
            name='NoteImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.note')),
            ],
        ),
    ]
