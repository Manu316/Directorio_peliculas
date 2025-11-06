# movies/urls.py

from django.urls import path
from . import views 
from .views import (
    UserCollectionView,
    MovieDetailView,
    MovieDeleteView,
)

urlpatterns = [
    path('', views.tmdb_home_view, name='home'),

    path('collection/', UserCollectionView.as_view(), name='collection_list'),
    
    # Búsqueda
    path('search/', views.search_movie, name='search_movie'),
    
    # Detalle de película
    path('detail/<int:pk>/', MovieDetailView.as_view(), name='detail_movie'),

    # Alternar el estado
    path('detail/<int:pk>/watched/', views.toggle_watched, name='toggle_watched'),
    
    # Eliminar una película
    path('detail/<int:pk>/delete/', MovieDeleteView.as_view(), name='delete_movie'),

    # Añadir desde TMDb
    path('add/', views.add_movie_from_tmdb, name='add_movie_from_tmdb'),

    # Detalle de TMDb
    path('tmdb/<int:tmdb_id>/', views.tmdb_detail, name='tmdb_detail'),

    # Rutas de Categorías
    path('peliculas/<slug:category>/',
         views.tmdb_category_list,
         {'media_type': 'movie'},
         name='tmdb_movies_category'),
         
    path('series/<slug:category>/',
         views.tmdb_category_list,
         {'media_type': 'tv'},
         name='tmdb_series_category'),

    path('play/<str:imdb_id>/', views.movie_player_view, name='movie_player'),
         
]