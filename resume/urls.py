from django.urls import path, include
from rest_framework.routers import DefaultRouter
from resume.views import ResumeViewSet, CorrectedResumeViewset

router = DefaultRouter()

router.register('resume', ResumeViewSet, basename='resume')
router.register('corrected', CorrectedResumeViewset, basename='corrected')

urlpatterns = [
    path('', include(router.urls)),
]
