# Generated by Django 4.2.1 on 2023-09-26 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('theblog', '0017_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='receiver_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
