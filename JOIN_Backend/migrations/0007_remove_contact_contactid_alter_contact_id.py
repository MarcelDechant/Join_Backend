# Generated by Django 5.1.3 on 2024-12-06 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JOIN_Backend', '0006_contact_contactid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='contactId',
        ),
        migrations.AlterField(
            model_name='contact',
            name='id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]