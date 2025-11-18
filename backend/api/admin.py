"""
Django Admin configuration for API models
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ResumeTemplate, UserResume, ResumeSection, AIEnhancement


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model"""

    list_display = ['email', 'full_name', 'subscription_tier', 'is_active', 'date_joined']
    list_filter = ['subscription_tier', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'location')}),
        ('Profile', {'fields': ('professional_summary', 'linkedin_url', 'github_url', 'portfolio_url')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Subscription', {'fields': ('subscription_tier', 'ai_enhancements_used_today', 'ai_enhancements_last_reset')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    readonly_fields = ['date_joined', 'updated_at', 'last_login']


@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    """Admin configuration for ResumeTemplate model"""

    list_display = ['template_id', 'name', 'category', 'is_active', 'is_premium', 'usage_count', 'rating']
    list_filter = ['category', 'is_active', 'is_premium']
    search_fields = ['name', 'template_id', 'description']
    readonly_fields = ['usage_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Info', {'fields': ('template_id', 'name', 'description', 'category')}),
        ('Template Content', {'fields': ('html_structure', 'css_styling')}),
        ('Media', {'fields': ('preview_image', 'thumbnail')}),
        ('Features', {'fields': ('is_active', 'is_premium', 'supports_photo', 'supports_colors')}),
        ('Statistics', {'fields': ('usage_count', 'rating')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(UserResume)
class UserResumeAdmin(admin.ModelAdmin):
    """Admin configuration for UserResume model"""

    list_display = ['title', 'user', 'template', 'is_active', 'is_public', 'created_at', 'updated_at']
    list_filter = ['is_active', 'is_public', 'created_at']
    search_fields = ['title', 'user__email', 'public_slug']
    readonly_fields = ['view_count', 'download_count', 'created_at', 'updated_at', 'public_slug']
    raw_id_fields = ['user', 'template']

    fieldsets = (
        ('Basic Info', {'fields': ('user', 'template', 'title')}),
        ('Resume Data', {'fields': ('resume_data_json',)}),
        ('Customization', {'fields': ('custom_colors', 'custom_fonts')}),
        ('Visibility', {'fields': ('is_active', 'is_public', 'public_slug')}),
        ('Files', {'fields': ('pdf_file', 'docx_file')}),
        ('Analytics', {'fields': ('view_count', 'download_count')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(ResumeSection)
class ResumeSectionAdmin(admin.ModelAdmin):
    """Admin configuration for ResumeSection model"""

    list_display = ['section_title', 'resume', 'section_type', 'order', 'is_visible', 'updated_at']
    list_filter = ['section_type', 'is_visible']
    search_fields = ['section_title', 'resume__title']
    raw_id_fields = ['resume']

    fieldsets = (
        ('Basic Info', {'fields': ('resume', 'section_type', 'section_title')}),
        ('Content', {'fields': ('content',)}),
        ('Display', {'fields': ('order', 'is_visible')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    readonly_fields = ['created_at', 'updated_at']


@admin.register(AIEnhancement)
class AIEnhancementAdmin(admin.ModelAdmin):
    """Admin configuration for AIEnhancement model"""

    list_display = ['user', 'enhancement_type', 'section_type', 'was_accepted', 'confidence_score', 'created_at']
    list_filter = ['enhancement_type', 'was_accepted', 'user_feedback', 'created_at']
    search_fields = ['user__email', 'original_text', 'enhanced_text']
    readonly_fields = ['created_at', 'accepted_at']
    raw_id_fields = ['user', 'resume']

    fieldsets = (
        ('Basic Info', {'fields': ('user', 'resume', 'section_type', 'enhancement_type')}),
        ('Text', {'fields': ('original_text', 'enhanced_text')}),
        ('AI Metadata', {'fields': ('confidence_score', 'model_used', 'prompt_tokens', 'completion_tokens')}),
        ('User Interaction', {'fields': ('was_accepted', 'accepted_at', 'user_feedback')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
