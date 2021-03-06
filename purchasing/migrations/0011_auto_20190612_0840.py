# Generated by Django 2.2 on 2019-06-12 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0010_auto_20190528_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmin73',
            name='c_asterik',
            field=models.CharField(blank=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='tmin72',
            name='i_itemno',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='tmin73',
            name='c_cert',
            field=models.CharField(blank=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='tmin73',
            name='c_cond',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='tmin73',
            name='c_e',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='tmin73',
            name='i_qacc',
            field=models.FloatField(blank=True),
        ),
    ]
