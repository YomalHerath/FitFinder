# Generated by Django 4.2.3 on 2023-12-27 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_thread_replies_thread_image_thread_tid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='description',
            field=models.TextField(blank=True, default='This is thread description', null=True),
        ),
    ]