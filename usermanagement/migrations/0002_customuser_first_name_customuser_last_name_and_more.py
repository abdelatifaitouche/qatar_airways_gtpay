# Generated by Django 4.2.9 on 2024-01-14 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(default='ali haouchine', max_length=255),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default='ali haouchine', max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='matricule',
            field=models.CharField(default=None, max_length=8),
        ),
    ]
