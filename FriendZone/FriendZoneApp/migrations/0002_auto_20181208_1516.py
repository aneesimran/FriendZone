# Generated by Django 2.1.3 on 2018-12-08 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FriendZoneApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='image',
            field=models.ImageField(blank=True, default='default.png', upload_to='media/profile_images'),
        ),
    ]