# Generated by Django 4.1.7 on 2023-07-08 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbhome', '0011_alter_profile_bio_alter_profile_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
