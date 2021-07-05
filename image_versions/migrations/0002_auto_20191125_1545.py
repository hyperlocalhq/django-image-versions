# Generated by Django 2.2.3 on 2019-11-25 14:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_versions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='focuspoint',
            name='x',
            field=models.FloatField(default=0, help_text='From -1.0 (left) to 1.0 (right)', validators=[django.core.validators.MinValueValidator(-1.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='X'),
        ),
        migrations.AlterField(
            model_name='focuspoint',
            name='y',
            field=models.FloatField(default=0, help_text='From -1.0 (bottom) to 1.0 (top)', validators=[django.core.validators.MinValueValidator(-1.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='Y'),
        ),
    ]
