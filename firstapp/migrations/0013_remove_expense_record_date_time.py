# Generated by Django 5.0.1 on 2024-03-29 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0012_remove_friends_record_owed_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense_record',
            name='date_time',
        ),
    ]