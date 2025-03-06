from rest_framework.routers import DefaultRouter

from app.views import AuthorViewSet, BookViewSet

router = DefaultRouter()

router.register("authors", AuthorViewSet, basename="authors")
router.register("books", BookViewSet, basename="books")


urlpatterns = router.urls
