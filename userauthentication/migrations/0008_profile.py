# Generated by Django 4.2.3 on 2024-01-01 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauthentication', '0007_alter_contactus_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image')),
                ('full_name', models.CharField(max_length=200)),
                ('bio', models.CharField(blank=True, max_length=300, null=True)),
                ('phone', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
    ]
