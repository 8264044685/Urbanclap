# Generated by Django 2.2 on 2020-02-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200216_0641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicesprovider',
            name='user',
        ),
        migrations.AddField(
            model_name='servicesprovider',
            name='full_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
