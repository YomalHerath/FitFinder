# Generated by Django 4.2.3 on 2023-12-26 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_contactus'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContactUs',
            new_name='Contact',
        ),
    ]