# Generated by Django 4.1.7 on 2023-07-29 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbhome', '0037_alter_query_cemail_alter_query_cfname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='replied_by',
            field=models.EmailField(blank=True, default='-1', max_length=100),
        ),
    ]
