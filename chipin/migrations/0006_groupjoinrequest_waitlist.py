# Generated by Django 5.1.5 on 2025-03-21 22:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chipin', '0005_event'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='groupjoinrequest',
            name='waitlist',
            field=models.ManyToManyField(blank=True, related_name='waitlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
