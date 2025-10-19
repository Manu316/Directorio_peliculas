from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Movie
import requests

# --- CRUD  ---

# Lista de Películas
class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    ordering = ['title']

# Eliminar Película
class MovieDeleteView(DeleteView):
    model = Movie
    success_url = reverse_lazy('list_movies') 
    template_name = 'movies/movie_confirm_delete.html'


# --- Manejo de Estado ---

# Alterna el estado 'watched'
def toggle_watched(request, pk):
    
    movie = get_object_or_404(Movie, pk=pk)
    movie.watched = not movie.watched  
    movie.save()
    # Redirige a la página de detalle de la película
    return redirect('detail_movie', pk=pk)


# --- Integración con API  ---

# Detalle de Película
class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = context['movie']
        
        # --- Integración con TMDb ---

        TMDB_API_KEY = '3413fa4f67aeac0d92813af9cd5aa642' 
        
        # Llamada a la API para obtener datos
        url = f"https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={TMDB_API_KEY}&language=es-ES"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            api_data = response.json()
            context['api_data'] = api_data 

        except requests.exceptions.RequestException as e:
            # Manejo básico de errores
            context['api_error'] = f"Error al obtener datos de TMDb: {e}"

        return context


#Búsqueda de Películas
def search_movie(request):
    results = []
    query = request.GET.get('q')
    
    if query:
        TMDB_API_KEY = '3413fa4f67aeac0d92813af9cd5aa642' 
        # Endpoint para buscar por título
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=es-ES"
        
        try:
            response = requests.get(url)
            response.raise_for_status() 
            api_results = response.json().get('results', [])
            
            # Filtra solo los resultados con póster y fecha de lanzamiento
            results = [
                r for r in api_results 
                if r.get('poster_path') and r.get('release_date')
            ][:10] 

        except requests.exceptions.RequestException as e:
            pass

    return render(request, 'movies/movie_search.html', {'results': results, 'query': query})