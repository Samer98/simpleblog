# Generated by Django 4.2.1 on 2023-09-25 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0015_comment_date_added_alter_comment_body'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='comment',
        ),
    ]
