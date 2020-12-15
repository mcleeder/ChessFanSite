# Generated by Django 2.2.5 on 2020-12-09 20:19

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChessGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=120)),
                ('time_control', models.CharField(max_length=60)),
                ('end_time', models.DateField()),
                ('rated', models.BooleanField()),
                ('fen', models.CharField(max_length=120)),
                ('time_class', models.CharField(max_length=60)),
                ('rules', models.CharField(max_length=60)),
                ('white_player', models.CharField(max_length=120)),
                ('white_player_rating', models.CharField(max_length=10)),
                ('white_player_result', models.CharField(max_length=30)),
                ('black_player', models.CharField(max_length=120)),
                ('black_player_rating', models.CharField(max_length=10)),
                ('black_player_result', models.CharField(max_length=30)),
            ],
            managers=[
                ('Games', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ChessGameGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('player1', models.CharField(max_length=120)),
                ('player2', models.CharField(max_length=120)),
                ('game_list1', models.ManyToManyField(to='ChessApp.ChessGame')),
            ],
            managers=[
                ('Groups', django.db.models.manager.Manager()),
            ],
        ),
    ]