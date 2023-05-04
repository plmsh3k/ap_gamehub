"""Defines URL patterns for learning_logs."""

from django.urls import path
from . import views
app_name = "gamehubs"
urlpatterns = [
    #Home page
    path('', views.index, name='index'),
    path('homepage/', views.homepage, name='games'),
    path('homepage/<int:game_id>/', views.game, name='game'),
    #adding new books
    path('profile/', views.profile, name='profile'),
    path('game/<int:game_id>/scores/', views.game_scores, name='game_scores'),
    path('new_review/<int:game_id>/', views.new_review, name='new_review'),
    #path('edit_review/<int:review_id>/', views.edit_review, name='edit_review')
]
