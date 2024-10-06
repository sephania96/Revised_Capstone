from rest_framework import serializers
from .models import Movie, Review
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)  # Display the movie title
    user = serializers.CharField(source='user.username', read_only=True)  # Display the user name of the person creating the review

    class Meta:
        model = Review
        fields = ['id', 'movie', 'movie_title', 'review_content', 'rating', 'user', 'created_date']
        read_only_fields = ['user', 'created_date', 'movie_title']

    def create(self, validated_data):
        movie = validated_data.pop('movie')  # Extract movie data
        review = Review.objects.create(movie=movie, **validated_data)
        return review


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date']


