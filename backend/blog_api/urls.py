from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('posts/', views.posts_view, name='posts'),
    path('posts/<int:post_id>/', views.posts_view, name='post_detail'),
    path('verify-token/', views.verify_token_view, name='verify_token'),
]