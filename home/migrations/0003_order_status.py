# Generated by Django 5.0.4 on 2024-04-28 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_order_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
