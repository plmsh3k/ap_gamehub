import random

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Game, GameReview, Score
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ReviewForm
from random import randint
from django.db.models import Max



def index(request):
    return render(request, 'gamehubs/index.html')

def homepage(request):
    games = Game.objects.all()
    context = {'games':games}
    return render(request, 'gamehubs/homepage.html', context)


def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    calculate_game_rating(game_id)

    # Get the top score for each user on this game
    high_scores = Score.objects.filter(game=game).values('user__username').annotate(max_score=Max('points'))

    # Get the scores for the current user on this game
    try:
        user_score = Score.objects.get(user=request.user, game=game)
    except Score.DoesNotExist:
        user_score = None

    if request.method == 'POST':
        # Handle form submission
        score_value = random.randint(1, 1000)
        score, created = Score.objects.get_or_create(user=request.user, game=game)
        if score_value > score.points:
            score.points = score_value
            score.save()

        return HttpResponseRedirect(reverse('gamehubs:game', args=[game_id]))
    else:
        # Render game page with "play" button
        reviews = GameReview.objects.filter(game=game)
        high_scores = [{'username': score['user__username'], 'max_score': score['max_score']} for score in high_scores]
        context = {'game': game, 'reviews': reviews, 'form': ReviewForm(),
                   'high_scores': high_scores, 'user_score': user_score}
        return render(request, 'gamehubs/game.html', context)


@login_required
def profile(request):
    user_scores = Score.objects.filter(user=request.user).select_related('game').order_by('-points')
    games_played = set(score.game for score in user_scores)

    past_games = list(games_played)
    high_scores = []
    for game in games_played:
        high_score = Score.objects.filter(game=game, user=request.user).order_by('-points').first()
        if high_score:
            high_scores.append(high_score)

    context = {
        'past_games': past_games,
        'high_scores': high_scores,
    }
    return render(request, 'gamehubs/profile.html', context)




@login_required
def game_scores(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    user_scores = Score.objects.filter(game=game, user=request.user).order_by('-points')
    reviews = GameReview.objects.filter(game=game, user=request.user)

    context = {
        'game': game,
        'scores': user_scores,
        'reviews': reviews,
    }
    return render(request, 'gamehubs/game_scores.html', context)



@login_required
def new_review(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            return HttpResponseRedirect(reverse('gamehubs:game', args=[game_id]))
    else:
        form = ReviewForm()

    context = {'game': game, 'form': form}
    calculate_game_rating(game_id)
    return render(request, 'gamehubs/new_review.html', context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(GameReview, id=review_id)

    if request.user != review.user:
        # User does not have permission to edit this review
        return HttpResponseRedirect(reverse('gamehubs:game', args=[review.game.id]))

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gamehubs:game', args=[review.game.id]))
    else:
        form = ReviewForm(instance=review)

    context = {'game': review.game, 'form': form, 'review': review}
    return render(request, 'gamehubs/edit_review.html', context)


def calculate_game_rating(game_id):
    ratings = GameReview.objects.filter(game=game_id)
    if ratings:
        avg_rating = sum([rating.rating for rating in ratings])/len(ratings)
        game = Game.objects.get(id=game_id)
        game.rating = round(avg_rating, 1)
        game.save()
    else:
        game = Game.objects.get(id=game_id)
        game.rating = 0
        game.save()

