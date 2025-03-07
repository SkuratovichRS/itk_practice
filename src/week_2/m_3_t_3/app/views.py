from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from app.models import Author, Book
from app.serializers import AuthorSerializer, BookSerializer


class BookViewSetPagination(
    PageNumberPagination
):  # It feels unnecessary to create a separate module
    page_size = 5


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.prefetch_related("books").all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["id", "first_name", "last_name"]
    ordering_fields = ["id", "first_name", "last_name"]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    pagination_class = BookViewSetPagination


class BuyBookView(APIView):
    def post(self, request, pk):
        with transaction.atomic():
            book = get_object_or_404(
                Book.objects.select_for_update(), pk=pk, count__gt=0
            )
            book.count -= 1
            book.save()
        return Response({"message": "Book bought successfully"}, status=HTTP_200_OK)
