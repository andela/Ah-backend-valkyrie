# Generated by Django 2.1.4 on 2019-01-23 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20190123_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]