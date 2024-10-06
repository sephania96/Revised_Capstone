from django.shortcuts import render
from rest_framework import generics
from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend




class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Allow anyone to register
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Signup a new user", operation_description="Register a new user account.")
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "User created successfully", "user": response.data}, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return []
        return super().get_permissions()
    

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'username': user.username,
                'token': token.key}, 
                status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


## View to list or create reviews 
class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    

    def perform_create(self, serializer):
        # Automatically associate the review with the logged-in user and validate the movie exists
        movie_id = self.request.data.get('movie')  # Get the movie ID from request
        try:
            movie = Movie.objects.get(id=movie_id)
            # Set the user who created the review as the logged-in user
            serializer.save(user=self.request.user, movie=movie)
        except Movie.DoesNotExist:
            raise Response({"error": "Movie does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="List all reviews", operation_description="Retrieve all reviews for movies.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a review", operation_description="Create a new review for a movie.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


## View to fetch details of a particular review
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @swagger_auto_schema(operation_summary="Retrieve a review", operation_description="Retrieve details of a specific review.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update a review", operation_description="Update an existing review.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a review", operation_description="Delete an existing review.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


## View to add pagination to Reviews List 
class ReviewPagination(PageNumberPagination):
    page_size = 5  # Number of reviews per page
    page_size_query_param = 'page_size'
    max_page_size = 10



## View to fetch reviews by Movie title 
class ReviewSearchFilter(generics.ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    # Adding the search and filtering backends
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    # Allowing searching by movie title
    search_fields = ['movie__movie_title']  # Searching in the related 'movie' field
    search_param = 'movie_title'
    
    # Allowing filtering by rating
    filterset_fields = ['rating']  # Optional filtering by rating (1-5)
    
    def get_queryset(self):
        """
        Optionally restricts the returned reviews to a given movie title or rating,
        by filtering against query parameters in the URL.
        """
        queryset = Review.objects.all()  # Base queryset for all reviews
        
        # Extract query parameters
        movie_title = self.request.query_params.get('movie_title', None)
        rating = self.request.query_params.get('rating', None)

        # Filter by movie title if provided
        if movie_title:
            queryset = queryset.filter(movie__movie_title__icontains=movie_title)
        
        # Filter by rating if provided
        if rating:
            queryset = queryset.filter(rating=rating)
        
        return queryset

    
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('movie_title', openapi.IN_QUERY, description="Search by movie title", type=openapi.TYPE_STRING),
        openapi.Parameter('rating', openapi.IN_QUERY, description="Filter by rating (1-5)", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

   



class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @swagger_auto_schema(operation_summary="List all movies", operation_description="Retrieve all movies.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a movie", operation_description="Create a new movie.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)




class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @swagger_auto_schema(operation_summary="Retrieve a movie", operation_description="Retrieve details of a specific movie.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update a movie", operation_description="Update an existing movie.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a movie", operation_description="Delete an existing movie.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
