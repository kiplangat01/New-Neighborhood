# Generated by Django 4.0.4 on 2022-06-20 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0002_rename_photo_neighbourhood_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='neighborhood',
            new_name='neighbourhood',
        ),
    ]