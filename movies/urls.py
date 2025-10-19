# movies/urls.py

from django.urls import path
from . import views 

urlpatterns = [
    # Vista de inicio
    path('', views.MovieListView.as_view(), name='list_movies'),

    # Vista de búsqueda
    path('search/', views.search_movie, name='search_movie'),

    # Rutas
    path('<int:pk>/', views.MovieDetailView.as_view(), name='detail_movie'),
    path('<int:pk>/watched/', views.toggle_watched, name='toggle_watched'),
]