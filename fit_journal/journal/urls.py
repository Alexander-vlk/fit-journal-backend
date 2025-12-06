from django.urls import path, include
from rest_framework.routers import SimpleRouter

from journal.views import (
    ExerciseViewSet,
    TrainingCreate,
    ExerciseSetViewSet,
    GetColorsList,
    AthleteTrainingTypeColorViewSet,
    CompareTraining,
)

journal_router = SimpleRouter()
journal_router.register('exercises', ExerciseViewSet)
journal_router.register('exercise_sets', ExerciseSetViewSet, basename='exercise_set')
journal_router.register(
    'athlete_trainingtypes_colors',
    AthleteTrainingTypeColorViewSet,
    basename='athlete_trainingtypes_colors',
)

urlpatterns = [
    path('', include(journal_router.urls)),
    path('training/', TrainingCreate.as_view(), name='training_create'),
    path('training/compare/', CompareTraining.as_view(), name='training_compare'),
    path('color/', GetColorsList.as_view(), name='get_colors_list'),
]
