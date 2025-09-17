from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (BiomarkerViewSet, UserProfileViewSet, PublisherViewSet, CategoryViewSet, TagViewSet, BookViewSet, FeaturedBookViewSet, EBookViewSet, AuthorViewSet, ContributionViewSet, CommentViewSet)

router = DefaultRouter()
router.register(r"biomarkers", BiomarkerViewSet)
router.register(r"user-profiles", UserProfileViewSet)
router.register(r"publishers", PublisherViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"tags", TagViewSet)
router.register(r"books", BookViewSet)
router.register(r"featured-books", FeaturedBookViewSet, basename="featured-book")
router.register(r"ebooks", EBookViewSet)
router.register(r"authors", AuthorViewSet)
router.register(r"contributions", ContributionViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [path("", include(router.urls))]
