# Generated by Django 3.0.2 on 2020-08-31 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200831_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='serieseason',
            name='imdb',
            field=models.FloatField(default=0),
        ),
    ]
