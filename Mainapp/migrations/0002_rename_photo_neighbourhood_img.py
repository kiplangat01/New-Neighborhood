# Generated by Django 4.0.4 on 2022-06-20 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='neighbourhood',
            old_name='photo',
            new_name='img',
        ),
    ]
