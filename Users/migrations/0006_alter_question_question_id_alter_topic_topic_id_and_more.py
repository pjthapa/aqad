# Generated by Django 5.1.6 on 2025-02-26 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_alter_topic_subtopic_name_alter_topic_topic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='QUESTION_ID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='topic',
            name='TOPIC_ID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='USER_ID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
