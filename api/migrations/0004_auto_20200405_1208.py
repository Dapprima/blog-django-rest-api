# Generated by Django 3.0.5 on 2020-04-05 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200405_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='last_request',
            field=models.DateTimeField(),
        ),
    ]