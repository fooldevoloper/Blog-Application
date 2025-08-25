import os
import sys
import django
from django.contrib.auth import get_user_model
from django.conf import settings

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django

from blog_api.models import Post

def create_sample_data():
    User = get_user_model()
    
    # Create sample users
    users_data = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'password123'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'password123'
        },
        {
            'username': 'bob_wilson',
            'email': 'bob@example.com',
            'password': 'password123'
        }
    ]
    
    users = []
    for user_data in users_data:
        # Check if user already exists
        if not User.objects.filter(email=user_data['email']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            users.append(user)
            print(f"Created user: {user.username}")
        else:
            user = User.objects.get(email=user_data['email'])
            users.append(user)
            print(f"User already exists: {user.username}")
    
    # Create sample posts
    posts_data = [
        {
            'title': 'Getting Started with Django',
            'content': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the model-view-template architectural pattern and provides a robust set of tools for building web applications.',
            'author': user
        },
        {
            'title': 'Understanding React Hooks',
            'content': 'React Hooks are functions that let you "hook into" React state and lifecycle features from function components. They allow you to use state and other React features without writing a class. The most common hooks are useState, useEffect, and useContext.',
            'author': user
        },
        {
            'title': 'CSS Grid vs Flexbox',
            'content': 'CSS Grid and Flexbox are both powerful layout systems in CSS, but they serve different purposes. Grid is better for two-dimensional layouts (rows and columns), while Flexbox is better for one-dimensional layouts (either rows or columns). Understanding when to use each is key to modern CSS layout.',
            'author': user
        }
    ]
    
    for post_data in posts_data:
        # Check if post already exists
        if not Post.objects.filter(title=post_data['title']).exists():
            post = Post.objects.create(
                title=post_data['title'],
                content=post_data['content'],
                author=post_data['author']
            )
            print(f"Created post: {post.title}")
        else:
            print(f"Post already exists: {post_data['title']}")
    
    print("\nSample data creation completed!")

if __name__ == '__main__':
    create_sample_data()