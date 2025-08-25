import os
import sys
import django
from django.contrib.auth import get_user_model

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")

# Setup Django
django.setup()

from blog_api.models import Post


def create_sample_data():
    User = get_user_model()

    # Sample users
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'password': 'password123'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'password123'},
        {'username': 'bob_wilson', 'email': 'bob@example.com', 'password': 'password123'}
    ]

    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'username': user_data['username'],
                'password': user_data['password']
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
        users.append(user)

    # Assign the first user as author for all posts
    author = users[0]

    # Sample posts
    posts_data = [
        {
            'title': 'Getting Started with Django',
            'content': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.'
        },
        {
            'title': 'Understanding React Hooks',
            'content': 'React Hooks are functions that let you "hook into" React state and lifecycle features from function components.'
        },
        {
            'title': 'CSS Grid vs Flexbox',
            'content': 'CSS Grid and Flexbox are both powerful layout systems in CSS, but they serve different purposes.'
        }
    ]

    for post_data in posts_data:
        post, created = Post.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'content': post_data['content'],
                'author': author
            }
        )
        if created:
            print(f"Created post: {post.title}")
        else:
            print(f"Post already exists: {post.title}")

    print("\nSample data creation completed!")


if __name__ == "__main__":
    create_sample_data()
