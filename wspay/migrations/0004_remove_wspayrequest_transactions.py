# Generated by Django 4.0.1 on 2022-01-20 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wspay', '0003_rename_wspaytransaction_transactionhistory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wspayrequest',
            name='transactions',
        ),
    ]
