# Generated by Django 3.2.4 on 2021-06-22 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0003_artist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='artist_name',
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='albums.artist'),
            preserve_default=False,
        ),
    ]