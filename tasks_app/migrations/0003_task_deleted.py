# Generated by Django 2.2.12 on 2021-12-16 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0002_auto_20211216_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
