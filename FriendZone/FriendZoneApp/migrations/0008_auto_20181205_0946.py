# Generated by Django 2.1 on 2018-12-05 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FriendZoneApp', '0007_auto_20181205_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hobby',
            name='hobby',
            field=models.CharField(blank=True, choices=[('H1', 'Hobby 1'), ('H2', 'Hobby 2'), ('H3', 'Hobby 3')], default='', max_length=20),
        ),
    ]