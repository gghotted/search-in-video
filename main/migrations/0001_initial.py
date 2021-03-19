# Generated by Django 3.0.5 on 2020-04-13 16:24

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
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('video', models.FileField(null=True, upload_to='')),
                ('audio', models.FileField(null=True, upload_to='')),
                ('source_type', models.CharField(max_length=50)),
                ('youtube_link', models.CharField(max_length=255, null=True)),
                ('state', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('extracted_by', models.CharField(max_length=50)),
                ('start_at', models.TimeField()),
                ('end_at', models.TimeField()),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='main.Video')),
            ],
        ),
        migrations.CreateModel(
            name='Vertex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vertices', to='main.Word')),
            ],
        ),
    ]