# Generated by Django 5.0.2 on 2024-06-01 03:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0033_alter_expense_record_date_field_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense_record',
            name='time_field',
            field=models.TimeField(default=datetime.datetime(2024, 6, 1, 9, 5, 4, 881249), null=True),
        ),
        migrations.AlterField(
            model_name='group_expense_record',
            name='time_field',
            field=models.TimeField(default=datetime.datetime(2024, 6, 1, 9, 5, 4, 882243), null=True),
        ),
    ]
