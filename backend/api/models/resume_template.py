"""
Resume Template Model
"""
from django.db import models
from django.utils import timezone


class ResumeTemplate(models.Model):
    """Resume template with HTML structure and CSS styling"""

    TEMPLATE_CATEGORIES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('creative', 'Creative'),
        ('executive', 'Executive'),
        ('tech', 'Tech'),
        ('academic', 'Academic'),
        ('startup', 'Startup'),
        ('minimal', 'Minimal'),
        ('ats_friendly', 'ATS Friendly'),
        ('portfolio', 'Portfolio'),
    ]

    template_id = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=TEMPLATE_CATEGORIES)

    # Template structure
    html_structure = models.TextField(
        help_text="Jinja2 template with placeholders for resume data"
    )
    css_styling = models.TextField(
        help_text="CSS styles for the template"
    )

    # Preview and metadata
    preview_image = models.ImageField(
        upload_to='template_previews/',
        null=True,
        blank=True
    )
    thumbnail = models.ImageField(
        upload_to='template_thumbnails/',
        null=True,
        blank=True
    )

    # Template features
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    supports_photo = models.BooleanField(default=True)
    supports_colors = models.BooleanField(default=True)

    # Usage statistics
    usage_count = models.IntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0
    )

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resume_templates'
        verbose_name = 'Resume Template'
        verbose_name_plural = 'Resume Templates'
        ordering = ['-usage_count', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"

    def increment_usage(self):
        """Increment usage counter"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])
