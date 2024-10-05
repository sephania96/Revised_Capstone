from django.shortcuts import render
from rest_framework import generics
from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return []
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        # Automatically associate the review with the logged-in user
        movie_id = self.request.data.get('movie')  # Get the movie ID from request
        try:
            movie = Movie.objects.get(id=movie_id)
            # Set the user who created the review as the logged-in user
            serializer.save(user=self.request.user, movie=movie)
        except Movie.DoesNotExist:
            return Response({"error": "Movie does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(operation_summary="List all reviews", operation_description="Retrieve all reviews for movies.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @swagger_auto_schema(operation_summary="Create a review", operation_description="Create a new review for a movie.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



class PublicViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  # No authentication needed for this view


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @swagger_auto_schema(operation_summary="List all movies", operation_description="Retrieve all available movies.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a movie", operation_description="Create a new movie entry.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



