# Generated by Django 2.1.3 on 2018-12-05 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobby', models.CharField(blank=True, choices=[('Gaming', 'Gaming'), ('Sports', 'Sports'), ('Reading', 'Reading'), ('Hiking', 'Hiking'), ('Cycling', 'Cycling'), ('Photography', 'Photography'), ('Modelling', 'Modelling')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('f', 'Female')], max_length=1)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to='profile_images')),
                ('dob', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('hobby', models.ManyToManyField(blank=True, to='FriendZoneApp.Hobby')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
