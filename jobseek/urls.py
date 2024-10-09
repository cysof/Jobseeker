from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('company', views.CompanyViewSet, basename='company')
router.register('job', views.JobViewSet, basename='job')
router.register('jobskill', views.JobSkillViewSet, basename='jobskill')
router.register('skill', views.SkillViewSet, basename='skill')
router.register('user', views.CustomUserViewSet, basename='user')
router.register('application', views.ApplicationViewSet, basename='application')

urlpatterns = router.urls