from resume.models import ResumeFeedback, CorrectedResume
from rest_framework import serializers
from django.db.models import Q


class ResumeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeFeedback
        fields = ['id', 'resume_file', 'feedback', 'created_at']
        read_only_fields = ['created_at']


class CorrectedResumeSerializer(serializers.ModelSerializer):
    corrected_resume_text = serializers.CharField(read_only=True)

    class Meta:
        model = CorrectedResume
        fields = ["id", "original_resume", "corrected_resume_text", "created_at", "user"]
