from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now




class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Movie relationship
    review_content = models.TextField()  
    rating = models.IntegerField()  # Rating (out of 5)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.movie.title} review by {self.user.username}'


