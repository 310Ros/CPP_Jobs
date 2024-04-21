from django.contrib.auth.models import User
from django.db import models
import uuid

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    regtype = models.CharField(max_length=20, choices=[
        ('job_seeker', 'Job Seeker'),
        ('job_provider', 'Job Provider'),
    ])

    def __str__(self):
        return self.user.username
    
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4().hex[:8])
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    contact_information = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.job_id}"
    
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"Application for {self.job.title} by {self.name}"
    
