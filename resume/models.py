from django.db import models
from config.utils.file_size_restriction import validate_file_size

# Create your models here.
class ResumeFeedback(models.Model):
    resume_file = models.FileField(upload_to='media/', validators=[validate_file_size])
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("users.User", related_name='resumes', on_delete=models.CASCADE)

class CorrectedResume(models.Model):
    original_resume = models.FileField(upload_to='media/', validators=[validate_file_size]) 
    corrected_resume_text = models.TextField(blank=True)
    user = models.ForeignKey("users.User", related_name='correctedresumes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


