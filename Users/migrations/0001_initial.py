# Generated by Django 4.2.19 on 2025-02-08 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('QUESTION_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('QUESTION_NAME', models.CharField(help_text='Question Text', max_length=10000)),
                ('OPTION_ONE', models.CharField(help_text='First Answer Option', max_length=1000)),
                ('OPTION_TWO', models.CharField(help_text='Second Answer Option', max_length=1000)),
                ('OPTION_THREE', models.CharField(help_text='First Answer Option', max_length=1000)),
                ('OPTION_FOUR', models.CharField(help_text='Second Answer Option', max_length=1000)),
                ('EXPLANATION_ONE', models.TextField(help_text='Explanation For the First Answer')),
                ('EXPLANATION_TWO', models.TextField(help_text='Explanation For the Second Answer')),
                ('EXPLANATION_THREE', models.TextField(help_text='Explanation For the Third Answer')),
                ('EXPLANATION_FOUR', models.TextField(help_text='Explanation For the Fourth Answer')),
                ('CORRECT_ANSWER', models.SmallIntegerField(help_text='Correct Answer Choice', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('TOPIC_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('SUBJECT', models.CharField(help_text='Specific subject for the topic', max_length=100)),
                ('TOPIC_NAME', models.CharField(help_text='Name of the topic', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('USER_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('USER_FIRST_NAME', models.CharField(help_text="User's first Name", max_length=100)),
                ('USER_LAST_NAME', models.CharField(help_text="USer's last name", max_length=100)),
                ('TOPIC', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Users.topic')),
            ],
        ),
        migrations.CreateModel(
            name='User_Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ANSWERED_ON', models.DateTimeField(help_text='Timestamp For the last Time Question was Sent to the user', null=True)),
                ('CORRECTLY_ANSWERED', models.BooleanField(default=False, help_text='Has User ever answered correctly')),
                ('QUESTION_ID', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Users.question')),
                ('TOPIC', models.ForeignKey(help_text='The topic category for this questions', on_delete=django.db.models.deletion.RESTRICT, to='Users.topic')),
                ('USER_ID', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Users.user')),
            ],
            options={
                'ordering': ['ANSWERED_ON'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='TOPIC',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Users.topic'),
        ),
    ]
