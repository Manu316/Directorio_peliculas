# movies/urls.py

from django.urls import path
from . import views 
from .views import MovieListView, MovieDetailView, MovieDeleteView

urlpatterns = [
    # Vista de inicio
    path('', views.MovieListView.as_view(), name='list_movies'),

    # Vista de búsqueda
    path('search/', views.search_movie, name='search_movie'),

    # Rutas
    # Vista de Inicio 
    path('', MovieListView.as_view(), name='list_movies'),

    # Vista de Búsqueda
    path('search/', views.search_movie, name='search_movie'),

    # Detalle de una película
    path('<int:pk>/', MovieDetailView.as_view(), name='detail_movie'),

    # Alternar el estado
    path('<int:pk>/watched/', views.toggle_watched, name='toggle_watched'),
    
    # Eliminar una película
    path('<int:pk>/delete/', MovieDeleteView.as_view(), name='delete_movie'),

    path('add/', views.add_movie_from_tmdb, name='add_movie_from_tmdb'),
]