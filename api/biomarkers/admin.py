from django.contrib import admin
from .models import Biomarker, UserProfile, Publisher, Category, Tag, Book, Author, Contribution, EBook, Comment, FeaturedBook
for m in (Biomarker, UserProfile, Publisher, Category, Tag, Book, Author, Contribution, EBook, Comment, FeaturedBook):
    admin.site.register(m)
