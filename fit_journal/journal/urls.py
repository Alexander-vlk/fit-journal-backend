from django.urls import path, include
from rest_framework.routers import SimpleRouter

from journal.views import ExerciseViewSet, TrainingCreate

journal_router = SimpleRouter()
journal_router.register('exercises', ExerciseViewSet)

urlpatterns = [
    path('', include(journal_router.urls)),
    path('training/', TrainingCreate.as_view(), name='training_create'),
]
