
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from .views import ReviewListCreate, ReviewDetail, MovieListCreate, MovieDetail, SignupView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'reviews', ReviewListCreate)
# router.register(r'movies', MovieViewSet)
router.register(r'users', views.UserViewSet)



urlpatterns = [
    path('reviews/', ReviewListCreate.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('movies/', MovieListCreate.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
# urlpatterns += router.urls