# Generated by Django 5.1.6 on 2025-02-12 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_topic_subtopic_name_alter_question_question_name_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user_question',
            unique_together={('USER_ID', 'QUESTION_ID')},
        ),
    ]
