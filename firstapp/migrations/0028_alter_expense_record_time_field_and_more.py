# Generated by Django 5.0.2 on 2024-05-31 14:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0027_alter_expense_record_time_field_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense_record',
            name='time_field',
            field=models.TimeField(default=datetime.datetime(2024, 5, 31, 19, 46, 26, 956414), null=True),
        ),
        migrations.AlterField(
            model_name='group_expense_record',
            name='time_field',
            field=models.TimeField(default=datetime.datetime(2024, 5, 31, 19, 46, 26, 957420), null=True),
        ),
    ]
