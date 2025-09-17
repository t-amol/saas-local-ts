from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (Biomarker, UserProfile, Publisher, Category, Tag, Book, Author, Contribution, EBook, Comment, FeaturedBook)
from .serializers import (BiomarkerSerializer, UserProfileSerializer, PublisherSerializer, CategorySerializer, TagSerializer, BookSerializer, AuthorSerializer, ContributionSerializer, EBookSerializer, CommentSerializer)

class IsReadOnlyOrAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (request.user and request.user.is_authenticated)

class BiomarkerViewSet(viewsets.ModelViewSet):
    queryset = Biomarker.objects.all().order_by("-created_at")
    serializer_class = BiomarkerSerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["assay_type","code"]
    search_fields   = ["code","name","assay_type"]
    ordering_fields = ["created_at","code","name"]
    ordering        = ["-created_at"]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related("user").all().order_by("id")
    serializer_class = UserProfileSerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["user","user__username"]
    search_fields   = ["display_name","bio","user__username","user__email"]
    ordering_fields = ["id","user__username"]
    ordering        = ["id"]

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all().order_by("name")
    serializer_class = PublisherSerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name"]
    search_fields   = ["name","website"]
    ordering_fields = ["name","id"]
    ordering        = ["name"]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.select_related("parent").all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["parent"]
    search_fields   = ["name","parent__name"]
    ordering_fields = ["name","id"]
    ordering        = ["name"]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name"]
    search_fields   = ["name"]
    ordering_fields = ["name","id"]
    ordering        = ["name"]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("publisher").prefetch_related("categories","tags","authors").all().order_by("-published_on","title")
    serializer_class = BookSerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["publisher","categories","tags","authors","published_on"]
    search_fields   = ["title","isbn","publisher__name","authors__first_name","authors__last_name","tags__name","categories__name"]
    ordering_fields = ["published_on","title","id"]
    ordering        = ["-published_on","title"]

class FeaturedBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeaturedBook.objects.select_related("publisher").prefetch_related("tags").all().order_by("-published_on","title")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["publisher","tags","published_on"]
    search_fields   = ["title","publisher__name","tags__name"]
    ordering_fields = ["published_on","title","id"]
    ordering        = ["-published_on","title"]

class EBookViewSet(viewsets.ModelViewSet):
    queryset = EBook.objects.select_related("publisher").all().order_by("-published_on","title")
    serializer_class = EBookSerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["publisher","published_on"]
    search_fields   = ["title","isbn","publisher__name"]
    ordering_fields = ["published_on","title","id"]
    ordering        = ["-published_on","title"]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("last_name","first_name")
    serializer_class = AuthorSerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["first_name","last_name"]
    search_fields   = ["first_name","last_name"]
    ordering_fields = ["last_name","first_name","id"]
    ordering        = ["last_name","first_name"]

class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.select_related("author","book").all().order_by("book_id","sort_order","id")
    serializer_class = ContributionSerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["author","book","role"]
    search_fields   = ["role","author__first_name","author__last_name","book__title","book__publisher__name"]
    ordering_fields = ["book_id","sort_order","id"]
    ordering        = ["book_id","sort_order","id"]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("content_type","author").all().order_by("-id")
    serializer_class = CommentSerializer
    permission_classes = [IsReadOnlyOrAuth]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["content_type","object_id","author"]
    search_fields   = ["body","author__username","author__email"]
    ordering_fields = ["id"]
    ordering        = ["-id"]
