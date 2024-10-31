from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, SubtaskViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'subtasks', SubtaskViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls)),
]