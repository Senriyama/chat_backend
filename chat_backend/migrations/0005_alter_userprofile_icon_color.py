# Generated by Django 5.0.4 on 2024-06-10 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_backend', '0004_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='icon_color',
            field=models.CharField(default='#E42222', max_length=7),
        ),
    ]