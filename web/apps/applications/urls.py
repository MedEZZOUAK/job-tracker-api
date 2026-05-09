from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, ApplicationNoteViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'notes', ApplicationNoteViewSet, basename='application-note')

urlpatterns = [
    path('', include(router.urls)),
]
