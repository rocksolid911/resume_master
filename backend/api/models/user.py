"""
User Model
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model with email as username"""

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True
    )
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)

    # Profile details
    professional_summary = models.TextField(blank=True)
    linkedin_url = models.URLField(max_length=500, blank=True)
    github_url = models.URLField(max_length=500, blank=True)
    portfolio_url = models.URLField(max_length=500, blank=True)

    # Account status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # AI Usage tracking
    ai_enhancements_used_today = models.IntegerField(default=0)
    ai_enhancements_last_reset = models.DateField(auto_now_add=True)

    # Subscription tier (for future use)
    subscription_tier = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('premium', 'Premium'),
            ('enterprise', 'Enterprise'),
        ],
        default='free'
    )

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def reset_ai_usage_if_needed(self):
        """Reset AI enhancement counter if a new day has started"""
        from datetime import date
        today = date.today()
        if self.ai_enhancements_last_reset < today:
            self.ai_enhancements_used_today = 0
            self.ai_enhancements_last_reset = today
            self.save(update_fields=['ai_enhancements_used_today', 'ai_enhancements_last_reset'])

    def can_use_ai_enhancement(self):
        """Check if user can use AI enhancement based on daily limit and subscription"""
        self.reset_ai_usage_if_needed()

        limits = {
            'free': 5,
            'premium': 50,
            'enterprise': 999999,
        }

        limit = limits.get(self.subscription_tier, 5)
        return self.ai_enhancements_used_today < limit

    def increment_ai_usage(self):
        """Increment AI enhancement usage counter"""
        self.ai_enhancements_used_today += 1
        self.save(update_fields=['ai_enhancements_used_today'])
