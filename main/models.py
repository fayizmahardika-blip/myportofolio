import uuid

from django.db import models
from django.contrib.auth.models import User

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]   
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    starred_by = models.ManyToManyField(
    User,
    related_name="starred_experiences",
    blank=True,
    )
    

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Education(models.Model):
    LEVEL_CHOICES = [
        ("junior-high", "Junior High School"),
        ("senior-high", "Senior High School"),
        ("undergraduate", "Undergraduate"),
    ]

    institution = models.CharField(max_length=255)
    level = models.CharField(
        max_length=30,
        choices=LEVEL_CHOICES
    )

    field_of_study = models.CharField(
        max_length=255,
        blank=True
    )

    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    grade = models.CharField(
        max_length=100,
        blank=True
    )

    activities = models.TextField(
        blank=True
    )

    achievements = models.TextField(
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    school_image = models.URLField(
        blank=True,
        null=True
    )

    school_url = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.institution

    @property
    def is_ongoing(self):
        return self.end_year is None



