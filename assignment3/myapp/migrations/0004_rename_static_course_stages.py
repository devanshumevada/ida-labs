# Generated by Django 4.0.5 on 2022-07-05 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_course_interested_course_static'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='static',
            new_name='stages',
        ),
    ]
