# Generated by Django 5.0.6 on 2024-09-18 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_service_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='reviews/'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
    ]
