from django.contrib import admin
from .models import Movie, Profile

# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'release_date', 'director', 'genre')
    list_filter = ('release_date', 'director', 'genre')
    search_fields = ('title', 'description', 'director', 'genre')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    search_fields = ('user__username', 'first_name', 'last_name', 'user__email')
