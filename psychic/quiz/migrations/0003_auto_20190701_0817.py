# Generated by Django 2.2.2 on 2019-07-01 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20190701_0722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='preference',
            new_name='prediction',
        ),
    ]
