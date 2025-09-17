from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class TimeStampedModel(models.Model):
    # Use auto_now_add / auto_now so fixtures don't need to supply created_at
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Biomarker(TimeStampedModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    assay_type = models.CharField(max_length=50)
    attributes = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.code


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.display_name


class Publisher(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    class Meta:
        unique_together = [("name", "parent")]

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Author(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(TimeStampedModel):
    title = models.CharField(max_length=255)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.PROTECT, related_name="books"
    )
    published_on = models.DateField()
    isbn = models.CharField(max_length=32, unique=True)
    categories = models.ManyToManyField(Category, related_name="books", blank=True)
    tags = models.ManyToManyField(Tag, related_name="books", blank=True)
    authors = models.ManyToManyField(Author, through="Contribution", related_name="books")

    def __str__(self):
        return self.title


class Contribution(TimeStampedModel):
    ROLE_CHOICES = [("AUTHOR", "Author"), ("EDITOR", "Editor")]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    sort_order = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = [("author", "book", "role")]


class EBook(Book):  # multi-table inheritance (extra table with same PK)
    file_url = models.URLField()
    file_size_bytes = models.BigIntegerField(default=0)


class Comment(TimeStampedModel):  # GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()


class FeaturedBook(Book):  # proxy model (no DB table)
    class Meta:
        proxy = True
