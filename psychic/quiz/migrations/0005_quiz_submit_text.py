# Generated by Django 2.2.2 on 2019-07-03 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='submit_text',
            field=models.TextField(default='Your response was recorded. Thank you!'),
        ),
    ]
