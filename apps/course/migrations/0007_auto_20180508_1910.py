# Generated by Django 2.0.4 on 2018-05-08 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20180507_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='organization.Teacher', verbose_name='课程讲师'),
        ),
    ]