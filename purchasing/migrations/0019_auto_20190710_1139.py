# Generated by Django 2.2 on 2019-07-10 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0018_auto_20190709_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmin73',
            name='c_cond',
            field=models.CharField(blank=True, default='', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tmin73',
            name='c_e',
            field=models.CharField(blank=True, default='', max_length=1),
            preserve_default=False,
        ),
    ]
