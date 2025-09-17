from rest_framework import serializers
from .models import Biomarker, UserProfile, Publisher, Category, Tag, Book, Author, Contribution, EBook, Comment

class BiomarkerSerializer(serializers.ModelSerializer):
    class Meta: model = Biomarker; fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")
    class Meta: model = UserProfile; fields = "__all__"

class PublisherSerializer(serializers.ModelSerializer):
    class Meta: model = Publisher; fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.ReadOnlyField(source="parent.name")
    class Meta: model = Category; fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta: model = Tag; fields = "__all__"

class AuthorSerializer(serializers.ModelSerializer):
    class Meta: model = Author; fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    class Meta: model = Book; fields = "__all__"

class ContributionSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source="author.__str__")
    book_title = serializers.ReadOnlyField(source="book.title")
    class Meta: model = Contribution; fields = "__all__"

class EBookSerializer(serializers.ModelSerializer):
    class Meta: model = EBook; fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    content_type_model = serializers.ReadOnlyField(source="content_type.model")
    author_username = serializers.ReadOnlyField(source="author.username")
    class Meta: model = Comment; fields = "__all__"
