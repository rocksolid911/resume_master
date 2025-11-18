"""
User Resume Model
"""
from django.db import models
from django.utils import timezone
from .user import User
from .resume_template import ResumeTemplate


class UserResume(models.Model):
    """User's resume with all data in JSON format"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resumes'
    )
    template = models.ForeignKey(
        ResumeTemplate,
        on_delete=models.SET_NULL,
        null=True,
        related_name='resumes'
    )

    # Resume metadata
    title = models.CharField(
        max_length=200,
        default='My Resume',
        help_text='Internal title for user reference'
    )

    # Resume data stored as JSON
    resume_data_json = models.JSONField(
        default=dict,
        help_text='Complete resume data in structured JSON format'
    )

    # Customization options
    custom_colors = models.JSONField(
        default=dict,
        blank=True,
        help_text='Custom color scheme for the resume'
    )
    custom_fonts = models.JSONField(
        default=dict,
        blank=True,
        help_text='Custom font settings'
    )

    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(
        default=False,
        help_text='Whether resume is publicly viewable via link'
    )
    public_slug = models.SlugField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text='Unique slug for public URL'
    )

    # File exports
    pdf_file = models.FileField(
        upload_to='resumes/pdf/%Y/%m/',
        null=True,
        blank=True
    )
    docx_file = models.FileField(
        upload_to='resumes/docx/%Y/%m/',
        null=True,
        blank=True
    )

    # Analytics
    view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_resumes'
        verbose_name = 'User Resume'
        verbose_name_plural = 'User Resumes'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['public_slug']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.title}"

    def save(self, *args, **kwargs):
        """Generate public slug if making resume public"""
        if self.is_public and not self.public_slug:
            import uuid
            self.public_slug = str(uuid.uuid4())[:12]
        super().save(*args, **kwargs)

    def increment_view_count(self):
        """Increment view counter"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def increment_download_count(self):
        """Increment download counter"""
        self.download_count += 1
        self.save(update_fields=['download_count'])

    @property
    def personal_info(self):
        """Extract personal information from resume data"""
        return self.resume_data_json.get('personal_info', {})

    @property
    def work_experience(self):
        """Extract work experience from resume data"""
        return self.resume_data_json.get('work_experience', [])

    @property
    def education(self):
        """Extract education from resume data"""
        return self.resume_data_json.get('education', [])

    @property
    def skills(self):
        """Extract skills from resume data"""
        return self.resume_data_json.get('skills', [])

    @property
    def projects(self):
        """Extract projects from resume data"""
        return self.resume_data_json.get('projects', [])
