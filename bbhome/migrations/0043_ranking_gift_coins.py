# Generated by Django 4.1.7 on 2023-08-17 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbhome', '0042_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranking',
            name='gift_coins',
            field=models.IntegerField(default=0),
        ),
    ]
