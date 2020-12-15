from django.db import models


# Create your models here.



class ChessGame(models.Model):
    url = models.CharField(max_length=120)
    time_control = models.CharField(max_length=60)
    end_time = models.DateField()
    rated = models.BooleanField()
    fen = models.CharField(max_length=120)
    time_class = models.CharField(max_length=60)
    rules = models.CharField(max_length=60)
    white_player = models.CharField(max_length=120)
    white_player_rating = models.CharField(max_length=10)
    white_player_result = models.CharField(max_length=30)
    black_player = models.CharField(max_length=120)
    black_player_rating = models.CharField(max_length=10)
    black_player_result = models.CharField(max_length=30)

    def __str__(self):
        return self.url

    Games = models.Manager()


class ChessGameGroup(models.Model):
    title = models.CharField(max_length=120)
    player1 = models.CharField(max_length=120)
    player2 = models.CharField(max_length=120)
    game_list1 = models.ManyToManyField(ChessGame)

    Groups = models.Manager()

