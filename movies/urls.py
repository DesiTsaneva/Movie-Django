from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.movie_search, name='movie_search'),
    path('add/', views.movie_add, name='movie_add'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('movie/<int:movie_id>/favorite/', views.movie_favorite, name='movie_favorite'),
    path('movie/<int:movie_id>/unfavorite/', views.movie_unfavorite, name='movie_unfavorite'),
    path('categories/', views.movie_categories, name='movie_categories'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.user_logout, name='logout'),
]
