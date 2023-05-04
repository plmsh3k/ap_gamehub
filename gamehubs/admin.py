from django.contrib import admin

# Register your models here.

from .models import Game, GameReview, Score

admin.site.register(GameReview)
admin.site.register(Game)
admin.site.register(Score)

