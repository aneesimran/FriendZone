# Generated by Django 2.1.3 on 2018-12-11 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FriendZoneApp', '0003_auto_20181208_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilemodel',
            name='friend',
            field=models.ManyToManyField(blank=True, related_name='_userprofilemodel_friend_+', to='FriendZoneApp.UserProfileModel'),
        ),
    ]
