from django.urls import path, include
from rest_framework.routers import DefaultRouter
from resume.views import ResumeViewSet

router = DefaultRouter()

router.register('resume', ResumeViewSet, basename='resume')

urlpatterns = [
    path('', include(router.urls)),
]
