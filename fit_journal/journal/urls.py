from django.urls import path

from journal.views import ExerciseList, ExerciseChangeView

urlpatterns = [
    path('journal/exercise/list', ExerciseList.as_view(), name='exercise_list'),
    path('journal/exercise/create/', ExerciseChangeView.as_view(), name='create_exercise'),
]
