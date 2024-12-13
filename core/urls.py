from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from django.contrib import admin
from django.urls import path, include

from student.views import StudentViewSet, GradesViewSet

router = DefaultRouter()
router.register(r"students", StudentViewSet)
router.register(r'grades', GradesViewSet, basename='sigaa-notas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f"api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/", include(router.urls)),
]
