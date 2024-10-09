from django.shortcuts import render
from rest_framework import viewsets
from .serializers import (CustomUserSerializer, 
                          CompanySerializer, 
                          JobSerializer, 
                          JobSkillSerializer, 
                          SkillSerializer, 
                          ApplicationSerializer)
from .models import Company, Job, JobSkill, Skill, Application, CustomUser
from rest_framework.decorators import action
from rest_framework.response import Response

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobSkillViewSet(viewsets.ModelViewSet):
    queryset = JobSkill.objects.all()
    serializer_class = JobSkillSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    @action(detail=False, methods=['get'])
    def get_by_user(self, request):
        user = request.user
        applications = Application.objects.filter(applicant_email=user.email)  # Ensure this is how you filter
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_by_user(self, request):
        user = request.user
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(applicant_email=user.email)  # Adjust as necessary based on your model
            return Response(serializer.data)
        return Response(serializer.errors)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=['get'])
    def get_current_user(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_by_user(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors)
