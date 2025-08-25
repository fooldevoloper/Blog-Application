import json
from django.forms.models import model_to_dict
from .models import User, Post


class UserSerializer:
    """
    Custom serializer for the User model.
    """
    
    @staticmethod
    def serialize(user):
        """
        Serialize a User instance to a dictionary.
        """
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    
    @staticmethod
    def serialize_many(users):
        """
        Serialize multiple User instances.
        """
        return [UserSerializer.serialize(user) for user in users]


class PostSerializer:
    """
    Custom serializer for the Post model.
    """
    
    @staticmethod
    def serialize(post):
        """
        Serialize a Post instance to a dictionary.
        """
        return {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at.isoformat()
        }
    
    @staticmethod
    def serialize_many(posts):
        """
        Serialize multiple Post instances.
        """
        return [PostSerializer.serialize(post) for post in posts]