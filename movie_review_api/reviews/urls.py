
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, MovieViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('movies/', views.MovieListCreateView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('', include(router.urls)),
]

urlpatterns += router.urls