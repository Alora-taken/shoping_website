# Generated by Django 5.0.1 on 2024-02-28 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_address_name_address_phone_address_postal_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
