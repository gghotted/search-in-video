# Generated by Django 3.0.5 on 2020-04-09 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_in_video', '0005_auto_20200402_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='state',
            field=models.CharField(default='complete', max_length=50),
            preserve_default=False,
        ),
    ]