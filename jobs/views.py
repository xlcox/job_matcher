from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resume, Vacancy
from .serializers import ResumeSerializer, VacancySerializer
from .utils import match_vacancy
from .permissions import IsAdmin, IsAdminOrCreateOnly


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAdminOrCreateOnly]


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAdmin]


@api_view(['GET'])
def match_resumes(request, vacancy_id):
    try:
        vac = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        return Response({'error': 'Vacancy not found'}, status=404)

    matches = match_vacancy(f"{vac.name}. {vac.description}",
                            Resume.objects.all())
    return Response([
        {'resume_id': r.id, 'score': s, 'text': r.text[:200] + '…'}
        for r, s in matches
    ])
