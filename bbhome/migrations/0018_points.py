# Generated by Django 4.1.7 on 2023-07-12 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbhome', '0017_delete_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='points',
            fields=[
                ('resultid', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=30)),
                ('right', models.IntegerField()),
                ('wrong', models.IntegerField()),
                ('n_a', models.IntegerField()),
                ('point', models.FloatField()),
                ('coins', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now=True)),
                ('quiztime', models.IntegerField()),
                ('time', models.TimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
