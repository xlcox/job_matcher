from rest_framework import serializers
from .models import CustomUser, Resume, Vacancy

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','full_name','phone_number','date_of_birth','is_admin']
        read_only_fields = ['is_admin']

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id','full_name','phone_number','mail','text']

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id','name','description']
