# Generated by Django 4.2.1 on 2023-06-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_botbutton'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Верификация пройдена'),
        ),
    ]