# Generated by Django 2.1.5 on 2019-01-30 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20190130_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tagList',
            field=models.ManyToManyField(blank=True, to='articles.Tag'),
        ),
    ]
