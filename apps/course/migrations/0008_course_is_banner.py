# Generated by Django 2.0.4 on 2018-05-09 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20180508_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否首页轮播'),
        ),
    ]