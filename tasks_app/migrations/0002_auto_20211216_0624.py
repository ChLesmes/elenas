# Generated by Django 2.2.12 on 2021-12-16 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
