"""
AI Enhancement Model
"""
from django.db import models
from django.utils import timezone
from .user import User
from .user_resume import UserResume


class AIEnhancement(models.Model):
    """Record of AI enhancements made to resume text"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ai_enhancements'
    )
    resume = models.ForeignKey(
        UserResume,
        on_delete=models.CASCADE,
        related_name='ai_enhancements',
        null=True,
        blank=True
    )

    # Enhancement details
    section_type = models.CharField(
        max_length=50,
        help_text='Type of section being enhanced'
    )
    enhancement_type = models.CharField(
        max_length=50,
        choices=[
            ('bullet_point', 'Bullet Point Enhancement'),
            ('description', 'Description Enhancement'),
            ('summary', 'Summary Generation'),
            ('grammar', 'Grammar & Style Improvement'),
            ('keywords', 'Keyword Optimization'),
            ('full_rewrite', 'Full Section Rewrite'),
        ],
        default='bullet_point'
    )

    # Original and enhanced text
    original_text = models.TextField()
    enhanced_text = models.TextField()

    # AI metadata
    confidence_score = models.FloatField(
        default=0.0,
        help_text='Confidence score from 0 to 1'
    )
    model_used = models.CharField(
        max_length=100,
        default='gpt-3.5-turbo',
        help_text='AI model used for enhancement'
    )
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)

    # User interaction
    was_accepted = models.BooleanField(
        default=False,
        help_text='Whether user accepted the enhancement'
    )
    user_feedback = models.CharField(
        max_length=20,
        choices=[
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('average', 'Average'),
            ('poor', 'Poor'),
        ],
        null=True,
        blank=True
    )

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'ai_enhancements'
        verbose_name = 'AI Enhancement'
        verbose_name_plural = 'AI Enhancements'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['resume', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.enhancement_type} ({self.created_at.date()})"

    def accept(self):
        """Mark enhancement as accepted"""
        self.was_accepted = True
        self.accepted_at = timezone.now()
        self.save(update_fields=['was_accepted', 'accepted_at'])
