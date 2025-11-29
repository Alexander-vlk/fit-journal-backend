from django.urls import path, include
from rest_framework.routers import SimpleRouter

from journal.views import ExerciseViewSet, TrainingCreate, ExerciseSetViewSet, GetColorsList

journal_router = SimpleRouter()
journal_router.register('exercises', ExerciseViewSet)
journal_router.register('exercise_sets', ExerciseSetViewSet, basename='exercise_set')

urlpatterns = [
    path('', include(journal_router.urls)),
    path('training/', TrainingCreate.as_view(), name='training_create'),
    path('color/', GetColorsList.as_view(), name='get_colors_list'),
]
