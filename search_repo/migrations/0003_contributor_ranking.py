# Generated by Django 2.1 on 2019-10-13 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_repo', '0002_auto_20191013_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='ranking',
            field=models.IntegerField(default=-2018),
            preserve_default=False,
        ),
    ]
