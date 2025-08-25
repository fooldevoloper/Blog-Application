import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import User, Post
from .serializers import UserSerializer, PostSerializer
from .utils.jwt_utils import generate_token, verify_token
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
import json


def get_user_from_token(request):
    """
    Extract and verify user from JWT token in Authorization header.
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    try:
        user_id = verify_token(token)
        return User.objects.get(id=user_id)
    except (User.DoesNotExist, ValidationError):
        return None


@csrf_exempt
def register_view(request):
    """
    Register a new user.
    POST /register/
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Serialize user data
        user_data = UserSerializer.serialize(user)
        
        return JsonResponse({
            'message': 'User registered successfully',
            'user': user_data
        }, status=201)
        
    except IntegrityError:
        return JsonResponse({'error': 'Username or email already exists'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Registration failed'}, status=500)


@csrf_exempt
def login_view(request):
    """
    Login user and return JWT token.
    POST /login/
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return JsonResponse({'error': 'Missing username or password'}, status=400)
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        # Generate JWT token
        token = generate_token(user.id)
        
        return JsonResponse({
            'message': 'Login successful',
            'token': token,
            'user': UserSerializer.serialize(user)
        })
        
    except Exception as e:
        return JsonResponse({'error': 'Login failed'}, status=500)


def list_posts_view(request):
    """
    List all posts.
    GET /posts/
    """
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    try:
        posts = Post.objects.all()
        posts_data = PostSerializer.serialize_many(posts)
        
        return JsonResponse({
            'posts': posts_data
        })
        
    except Exception as e:
        return JsonResponse({'error': 'Failed to fetch posts'}, status=500)


def post_detail_view(request, post_id):
    """
    Get details of a specific post.
    GET /posts/<id>/
    """
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    try:
        post = get_object_or_404(Post, id=post_id)
        post_data = PostSerializer.serialize(post)
        
        return JsonResponse({
            'post': post_data
        })
        
    except Exception as e:
        return JsonResponse({'error': 'Failed to fetch post'}, status=500)


@csrf_exempt
def create_post_view(request):
    """
    Create a new post.
    POST /posts/
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    # Verify authentication
    user = get_user_from_token(request)
    if not user:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        
        if not all([title, content]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Create post
        post = Post.objects.create(
            title=title,
            content=content,
            author=user
        )
        
        post_data = PostSerializer.serialize(post)
        
        return JsonResponse({
            'message': 'Post created successfully',
            'post': post_data
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'error': 'Failed to create post'}, status=500)


@csrf_exempt
def update_post_view(request, post_id):
    """
    Update a specific post.
    PUT /posts/<id>/
    """
    if request.method != 'PUT':
        return HttpResponseNotAllowed(['PUT'])
    
    # Verify authentication
    user = get_user_from_token(request)
    if not user:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        post = get_object_or_404(Post, id=post_id)
        
        # Check if user is the author
        if post.author != user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        
        # Update post
        if title:
            post.title = title
        if content:
            post.content = content
        post.save()
        
        post_data = PostSerializer.serialize(post)
        
        return JsonResponse({
            'message': 'Post updated successfully',
            'post': post_data
        })
        
    except Exception as e:
        return JsonResponse({'error': 'Failed to update post'}, status=500)


@csrf_exempt
def delete_post_view(request, post_id):
    """
    Delete a specific post.
    DELETE /posts/<id>/
    """
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])
    
    # Verify authentication
    user = get_user_from_token(request)
    if not user:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        post = get_object_or_404(Post, id=post_id)
        
        # Check if user is the author
        if post.author != user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Delete post
        post.delete()
        
        return JsonResponse({
            'message': 'Post deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': 'Failed to delete post'}, status=500)


@csrf_exempt
def posts_view(request, post_id=None):
    """
    Handle all post-related operations based on HTTP method and presence of post_id.
    """
    if request.method == 'GET' and post_id is None:
        # List all posts
        return list_posts_view(request)
    elif request.method == 'GET' and post_id is not None:
        # Get specific post
        return post_detail_view(request, post_id)
    elif request.method == 'POST' and post_id is None:
        # Create new post
        return create_post_view(request)
    elif request.method == 'PUT' and post_id is not None:
        # Update specific post
        return update_post_view(request, post_id)
    elif request.method == 'DELETE' and post_id is not None:
        # Delete specific post
        return delete_post_view(request, post_id)
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])


@csrf_exempt
def verify_token_view(request):
    """
    Verify JWT token and return user data.
    GET /verify-token/
    """
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    # Verify authentication
    user = get_user_from_token(request)
    if not user:
        return JsonResponse({'valid': False}, status=401)
    
    try:
        user_data = UserSerializer.serialize(user)
        return JsonResponse({
            'valid': True,
            'user': user_data
        })
    except Exception as e:
        return JsonResponse({'valid': False}, status=500)