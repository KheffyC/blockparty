# Generated by Django 4.1.2 on 2022-11-01 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profileimg',
            field=models.ImageField(default='regularprofileimage.jpeg', upload_to='profile_images'),
        ),
    ]