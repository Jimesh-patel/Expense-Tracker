# Generated by Django 3.2.6 on 2024-06-07 02:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0034_alter_expense_record_time_field_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense_record',
            name='date_field',
            field=models.DateField(default=datetime.date(2024, 6, 7), null=True),
        ),
        migrations.AlterField(
            model_name='expense_record',
            name='time_field',
            field=models.TimeField(default=datetime.datetime(2024, 6, 7, 8, 10, 48, 473461), null=True),
        ),
        migrations.AlterField(
            model_name='group_expense_record',
            name='date_field',
            field=models.DateField(default=datetime.date(2024, 6, 7), null=True),
        ),
        migrations.AlterField(
            model_name='group_expense_record',
            name='time_field',
            field=models.TimeField(default=datetime.datetime(2024, 6, 7, 8, 10, 48, 474558), null=True),
        ),
    ]
