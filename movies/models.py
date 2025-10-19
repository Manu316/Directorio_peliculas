from django.db import models
from django.urls import reverse

class Movie(models.Model):
    title = models.CharField(max_length=255)
    tmdb_id = models.IntegerField(unique=True) 
    release_date = models.DateField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    watched = models.BooleanField(default=False) 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail_movie', kwargs={'pk': self.pk})
