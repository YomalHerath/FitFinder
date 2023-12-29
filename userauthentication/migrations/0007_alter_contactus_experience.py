# Generated by Django 4.2.3 on 2023-12-29 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauthentication', '0006_contactus_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='experience',
            field=models.IntegerField(choices=[(1, 'Very Satisfied'), (2, 'Satisfied'), (3, 'Neutral'), (4, 'Dissatisfied'), (5, 'Very Dissatisfied')], default=None),
        ),
    ]
