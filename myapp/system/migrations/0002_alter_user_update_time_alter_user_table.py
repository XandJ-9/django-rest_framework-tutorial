# Generated by Django 4.2 on 2024-09-25 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterModelTable(
            name='user',
            table='sys_user',
        ),
    ]
