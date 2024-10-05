from rest_framework import serializers
from .models import Movie, Review
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date']

class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)  # Display the movie title

    class Meta:
        model = Review
        fields = ['id', 'movie', 'movie_title', 'review_content', 'rating', 'user', 'created_date']
        read_only_fields = ['user', 'created_at', 'movie_title']

    def create(self, validated_data):
        movie = validated_data.pop('movie')  # Extract movie data
        review = Review.objects.create(movie=movie, **validated_data)
        return review
