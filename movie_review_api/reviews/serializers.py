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
        # Create the user and set the password properly
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
    movie_title = serializers.ReadOnlyField(source='movie.movie_title')  # Display the movie title
    user = serializers.ReadOnlyField(source='user.username')  # Display the user name of the person creating the review

    class Meta:
        model = Review
        fields = ['id', 'movie', 'movie_title', 'review_content', 'rating', 'user', 'created_date']
        read_only_fields = ['user', 'created_date', 'movie_title']

    def create(self, validated_data):
        movie = validated_data.pop('movie')  # Extract movie data
        review = Review.objects.create(movie=movie, **validated_data)
        return review

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'movie_title', 'description', 'release_date']


