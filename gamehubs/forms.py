from django import forms

from .models import Game, GameReview, Score


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'creator', 'rating']
        labels = {'name': ''}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = GameReview
        fields = ['review', 'rating']
        labels = {'review': ''}
        

class Score(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['points']
        labels = {'points' : ''}
