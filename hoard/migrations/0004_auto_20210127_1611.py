# Generated by Django 3.1.5 on 2021-01-27 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoard', '0003_remove_order_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]