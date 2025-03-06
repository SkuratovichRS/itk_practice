from rest_framework import serializers

from app.models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["id"]


class AuthorBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title"]


class AuthorSerializer(serializers.ModelSerializer):
    books = AuthorBookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = "__all__"
        read_only_fields = ["id"]
