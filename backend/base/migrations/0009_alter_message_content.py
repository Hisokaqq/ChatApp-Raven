# Generated by Django 4.0.5 on 2023-02-16 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_message_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.CharField(max_length=10000),
        ),
    ]
