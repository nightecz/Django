# Generated by Django 5.1.2 on 2024-11-03 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0002_alter_movie_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.IntegerField(default=None),
        ),
    ]
