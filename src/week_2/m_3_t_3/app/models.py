from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="books")
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("title", "author")
