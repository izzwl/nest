# Generated by Django 2.2 on 2019-07-08 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0016_auto_20190618_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmin71',
            name='d_received',
            field=models.DateField(blank=True, null=True),
        ),
    ]
