from django.db import models
from django.utilis import timezone

# Create your models here.
class Job(models.Model):
    """
    Model representing a scraped job listing from LinkedIn.
    
    The job_id field serves as the business key for upsert operations.
    """
    # Unique identifier from LinkedIn (e.g., LinkedIn job posting ID)
    job_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Unique job identifier from LinkedIn"
    )

    # Job details
    title = models.CharField(
        max_length=500,
        help_text="Job title (e.g., 'Senior Backend Engineer')"
    )

    company = models.CharField(
        max_length=255,
        help_text="Company Name"
    )

    location = model.CharField(
        max_length=255,
        help_text="Job location (e.g., 'San Francisco, CA')"
    )

    description = model.TextField(
        help_text="Full job description"
    )

    # Metadata
    date_scraped = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when job was scraped"
    )

    date_updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of last update"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Record creation timestamp"
    )

    class Meta:
        db_table = 'jobs'
        ordering = ['-date_scraped']
        indexes = [
            models.Index(fields=['job_id'], name='job_id+idx'),
            models.Index(fields=['company'], name='company_idx'),
            models.Index(fields=['date_scraped'], name='date_scraped_idx')
        ]
        verbose_name = 'Job Listing'
        verbose_name_plural = 'Job Listings'

    def __str__(self):
        return f"{self.title} at {self.company}"
        ]
