# Generated by Django 4.2.3 on 2023-12-27 13:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_thread_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]