from resume.models import ResumeFeedback
from rest_framework import serializers
from django.db.models import Q


class ResumeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeFeedback
        fields = ['id', 'resume_file', 'feedback', 'created_at']
        read_only_fields = ['created_at']

