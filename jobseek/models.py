from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Experience Level
EXPERIENCE_LEVEL_CHOICES = (
    (0, 'Fresher'),
    (1, 'Entry Level'),
    (2, 'Mid Level'),
    (3, 'Senior Level'),
    (4, 'Lead Level'),
)

# Job Type
JOB_TYPE_CHOICES = (
    (0, 'Full Time'),
    (1, 'Part Time'),
    (2, 'Internship'),
    (3, 'Remote'),
    (4, 'Hybrid'),
    (5, 'On site'),
)

# Company model
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logo/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Skill model
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




# Job model
class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    job_type = models.IntegerField(choices=JOB_TYPE_CHOICES)
    experience_level = models.IntegerField(choices=EXPERIENCE_LEVEL_CHOICES)
    skills = models.ManyToManyField(Skill, through='JobSkill')
    salary = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# JobSkill model
class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return self.job.title

# Application model
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=100)
    applicant_email = models.EmailField()
    resume = models.FileField(upload_to='applications/')
    cover_letter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.applicant_name

# Custom User model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
