from .private import (
    TrainingCreate,
    ExerciseSetViewSet,
    AthleteTrainingTypeColorViewSet,
    CompareTraining,
)
from .public import ExerciseViewSet, GetColorsList

__all__ = [
    'AthleteTrainingTypeColorViewSet',
    'CompareTraining',
    'GetColorsList',
    'ExerciseSetViewSet',
    'ExerciseViewSet',
    'TrainingCreate',
]
