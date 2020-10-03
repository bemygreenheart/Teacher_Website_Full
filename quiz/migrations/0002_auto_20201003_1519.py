# Generated by Django 3.1.1 on 2020-10-03 15:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='article',
            new_name='quiz',
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('owner', 'quiz')},
        ),
    ]
