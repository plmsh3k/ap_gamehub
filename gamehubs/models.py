from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class GameReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(default="good")

    def __str__(self):
        return f"{self.game} - {self.rating}"


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    highest_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.game} - {self.user} - {self.points}"


