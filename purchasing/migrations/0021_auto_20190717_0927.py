# Generated by Django 2.2.3 on 2019-07-17 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0020_auto_20190711_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmin71',
            name='d_appr',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tmin72',
            name='d_appr',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tmin71',
            name='c_aju',
            field=models.CharField(blank=True, max_length=26),
        ),
    ]
