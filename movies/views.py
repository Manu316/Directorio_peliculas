# movies/views.py

import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.contrib import messages
from .models import Movie 

def tmdb_home_view(request):
    context = {}
    
    try:
        api_key = settings.TMDB_API_KEY 
        
        # Obtener películas Populares
        url_popular = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=es-ES&page=1"
        response_popular = requests.get(url_popular).json()
        context['popular_movies'] = response_popular.get('results', [])
        
        # Obtener películas en Cartelera
        url_now_playing = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=es-ES&page=1"
        response_now_playing = requests.get(url_now_playing).json()
        context['now_playing_movies'] = response_now_playing.get('results', [])
        
    except Exception as e:
        context['api_error'] = "No se pudieron cargar las listas de TMDb. Verifica tu API Key o conexión."
        
    return render(request, 'movies/tmdb_home.html', context)

class UserCollectionView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html' 
    context_object_name = 'movies'

# Vista de Detalle
class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        
        try:
            api_key = settings.TMDB_API_KEY
            url = f"https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={api_key}&language=es-ES"
            response = requests.get(url).json()
            context['api_data'] = response
        except Exception:
            context['api_error'] = "No se pudieron obtener datos adicionales de TMDb."
            
        return context

# Eliminar Película
class MovieDeleteView(DeleteView):
    model = Movie
    success_url = reverse_lazy('collection_list') 
    template_name = 'movies/movie_confirm_delete.html'

# Alternar estado Visto/Pendiente
def toggle_watched(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.watched = not movie.watched
    movie.save()
    messages.success(request, f"El estado de '{movie.title}' ha sido actualizado.")
    return redirect('detail_movie', pk=pk)

# Buscar Películas
def search_movie(request):
    query = request.GET.get('q')
    results = []
    
    existing_tmdb_ids = Movie.objects.values_list('tmdb_id', flat=True)

    existing_tmdb_ids_list = [str(tmdb_id) for tmdb_id in existing_tmdb_ids]
    
    if query:
        try:
            api_key = settings.TMDB_API_KEY
            url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}&language=es-ES"
            response = requests.get(url).json()
            results = response.get('results', [])
        except Exception as e:
            messages.error(request, "Error al conectar con TMDb.")

    context = {
        'results': results, 
        'query': query,
        'existing_tmdb_ids': existing_tmdb_ids_list,
    }

    return render(request, 'movies/movie_search.html', {'results': results, 'query': query})

# Añadir película
def add_movie_from_tmdb(request):
    if request.method == 'POST':
        tmdb_id = request.POST.get('tmdb_id')
        title = request.POST.get('title')
        
        release_date = request.POST.get('release_date')
        if not release_date: 
            release_date = None
            
        poster_path = request.POST.get('poster_path')

        if tmdb_id:
            if Movie.objects.filter(tmdb_id=tmdb_id).exists():
                messages.warning(request, f"'{title}' ya está en tu colección.")
                return redirect('collection_list') 

            try:
                Movie.objects.create(
                    tmdb_id=tmdb_id,
                    title=title,
                    release_date=release_date,
                    poster_path=poster_path,
                    watched=False
                )
                messages.success(request, f"¡'{title}' ha sido añadido a tu colección!")
            except Exception as e:
                messages.error(request, f"No se pudo guardar la película: {e}")

        return redirect('collection_list')
    
    messages.error(request, "Método no permitido.")
    return redirect('collection_list')

# Detalle de TMDb
def tmdb_detail(request, tmdb_id):
    api_key = settings.TMDB_API_KEY
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}&language=es-ES"
        response = requests.get(url).json()

        imdb_id = response.get('imdb_id')
        
        is_in_collection = Movie.objects.filter(tmdb_id=tmdb_id).exists()

        context = {
            'api_data': response,
            'is_in_collection': is_in_collection,
            'imdb_id': imdb_id
        }
    except Exception as e:
        context = {'error': f"Error al cargar el detalle de TMDb: {e}", 'imdb_id': None}

    return render(request, 'movies/tmdb_detail.html', context) 
    
def tmdb_category_list(request, media_type, category):
    api_key = settings.TMDB_API_KEY
    context = {}
    
    category_map = {
        'popular': 'popular',
        'proximo': 'upcoming',
        'mejor_calificado': 'top_rated'
    }

    tmdb_path = category_map.get(category)

    if tmdb_path:
        url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_path}?api_key={api_key}&language=es-ES&page=1"
        
        try:
            response = requests.get(url).json()
            results = response.get('results', [])
            
            context['media_list'] = results
            context['category_name'] = category.replace('_', ' ').title()
            context['media_type'] = media_type

        except Exception as e:
            context['api_error'] = f"Error al cargar {media_type} de TMDb: {e}"
    else:
        context['api_error'] = f"Categoría '{category}' no encontrada."

    return render(request, 'movies/tmdb_category_list.html', context)

# Reproductor de Películas
def movie_player_view(request, imdb_id):
    
    embed_url = f'https://vidlink.pro/movie/{imdb_id}'
    
    title = request.GET.get('title', 'Reproductor de Película')
    
    context = {
        'imdb_id': imdb_id,
        'embed_url': embed_url,
        'title': title, 
    }
    
    return render(request, 'movies/movie_player.html', context)    