# Generated by Django 3.2.12 on 2022-11-02 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileimg',
            field=models.ImageField(default='regularprofileimage.jpeg', upload_to='images/'),
        ),
    ]
