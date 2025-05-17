from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Resume, Vacancy
from .serializers import ResumeSerializer, VacancySerializer
from .utils import match_vacancy
from .permissions import IsAdminOrCreateOnly, IsAdmin


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
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        return Response({"error": "Vacancy not found"}, status=404)

    resumes = Resume.objects.all()
    matches = match_vacancy(f"{vacancy.name}. {vacancy.description}", resumes)

    return Response([
        {
            "resume_id": r.id,
            "score": s,
            "text": r.text[:300] + ("..." if len(r.text) > 300 else "")
        } for r, s in matches
    ])
