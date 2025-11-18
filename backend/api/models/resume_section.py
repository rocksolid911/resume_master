"""
Resume Section Model
"""
from django.db import models
from django.utils import timezone
from .user_resume import UserResume


class ResumeSection(models.Model):
    """Individual sections of a resume for detailed tracking"""

    SECTION_TYPES = [
        ('header', 'Header'),
        ('summary', 'Professional Summary'),
        ('experience', 'Work Experience'),
        ('education', 'Education'),
        ('skills', 'Skills'),
        ('projects', 'Projects'),
        ('certifications', 'Certifications'),
        ('languages', 'Languages'),
        ('awards', 'Awards & Achievements'),
        ('publications', 'Publications'),
        ('volunteer', 'Volunteer Experience'),
        ('references', 'References'),
        ('custom', 'Custom Section'),
    ]

    resume = models.ForeignKey(
        UserResume,
        on_delete=models.CASCADE,
        related_name='sections'
    )

    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    section_title = models.CharField(
        max_length=100,
        help_text='Display title for the section'
    )

    # Section content
    content = models.JSONField(
        default=dict,
        help_text='Section content in structured format'
    )

    # Section ordering and visibility
    order = models.IntegerField(
        default=0,
        help_text='Display order in resume'
    )
    is_visible = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resume_sections'
        verbose_name = 'Resume Section'
        verbose_name_plural = 'Resume Sections'
        ordering = ['resume', 'order']
        indexes = [
            models.Index(fields=['resume', 'order']),
        ]

    def __str__(self):
        return f"{self.resume.title} - {self.section_title}"
