# Generated by Django 4.0.4 on 2022-06-20 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0003_rename_neighborhood_profile_neighbourhood'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='neighborhood',
            new_name='neighbourhood',
        ),
        migrations.RenameField(
            model_name='updates',
            old_name='neighborhood',
            new_name='neighbourhood',
        ),
    ]
