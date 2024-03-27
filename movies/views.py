from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Movie, Profile
from django.db.models import Count
from .forms import RegistrationForm, EditProfileForm, MovieForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile
    favorites = profile.favorites.all()[:3]
    return render(request, 'registration/profile.html', {'profile': profile, 'favorites': favorites})

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'registration/edit_profile.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')





@login_required
def favorite_list(request):
    profile = request.user.profile
    favorites = profile.favorites.all()
    return render(request, 'movies/favorite_list.html', {'favorites': favorites})

@login_required
def movie_add(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movies/movie_add.html', {'form': form})

@login_required
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user_profile = request.user.profile
    is_favorite = movie in user_profile.favorites.all()
    context = {
        'movie': movie,
        'user_profile': user_profile,
        'is_favorite': is_favorite,
    }
    return render(request, 'movies/movie_detail.html', context)

@login_required
def movie_favorite(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    profile = request.user.profile
    profile.favorites.add(movie)
    return redirect('movie_detail', movie_id=movie_id)

@login_required
def movie_unfavorite(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    profile = request.user.profile
    profile.favorites.remove(movie)
    return redirect('movie_detail', movie_id=movie_id)


@login_required
def movie_search(request):
    title = request.GET.get('title', '')
    director = request.GET.get('director', '')
    genre = request.GET.get('genre', '')

    results = None
    query = {}

    if title or director or genre:
        results = Movie.objects.all()

        if title:
            results = results.filter(title__icontains=title)
            query['title'] = title
        if director:
            results = results.filter(director__icontains=director)
            query['director'] = director
        if genre:
            results = results.filter(genre__icontains=genre)
            query['genre'] = genre

    context = {
        'results': results,
        'query': query,
    }

    return render(request, 'movies/movie_search.html', context)




def movie_categories(request):
    # Get distinct genres
    genres = Movie.objects.values_list('genre', flat=True).distinct()

    # Create a dictionary to store top 5 movies for each genre
    top_movies_by_genre = {}
    for genre in genres:
        top_movies = Movie.objects.filter(genre=genre).order_by('-id')[:5]
        top_movies_by_genre[genre] = top_movies

    # Get top 5 most liked movies
    # most_liked_movies = Movie.objects.annotate(num_likes=Count('favorited_by')).order_by('-num_likes')[:5]
    # Get top 5 most liked movies with at least 1 favorite
    most_liked_movies = Movie.objects.annotate(num_likes=Count('favorited_by')).filter(num_likes__gt=0).order_by('-num_likes')[:5]

    # Get top 5 newest movies
    newest_movies = Movie.objects.order_by('-release_date')[:5]

    context = {
        'top_movies_by_genre': top_movies_by_genre,
        'most_liked_movies': most_liked_movies,
        'newest_movies': newest_movies,
    }
    return render(request, 'movies/movie_categories.html', context)