from django.db import models

# Create your models here.
class ResumeFeedback(models.Model):
    resume_file = models.FileField(upload_to='media/')
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)