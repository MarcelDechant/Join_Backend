# Generated by Django 5.1.3 on 2024-12-06 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JOIN_Backend', '0002_rename_email_contact_add_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='contacts',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='task',
            name='subtasks',
            field=models.JSONField(default=list),
        ),
    ]
