# Generated by Django 3.0.3 on 2020-03-22 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_in_video', '0003_auto_20200322_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='title',
            field=models.CharField(default='cnn-김성훈', max_length=100),
            preserve_default=False,
        ),
    ]
