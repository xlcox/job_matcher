from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, VacancyViewSet, match_resumes

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet)
router.register(r'vacancies', VacancyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('match/<int:vacancy_id>/', match_resumes),
]
