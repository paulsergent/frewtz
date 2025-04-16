# Generated by Django 5.1.7 on 2025-04-16 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='ordered_date',
        ),
        migrations.AddField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
