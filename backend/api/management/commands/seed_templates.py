"""
Management command to seed resume templates
Run with: python manage.py seed_templates
"""
from django.core.management.base import BaseCommand
from api.models import ResumeTemplate
import os


class Command(BaseCommand):
    help = 'Seed resume templates into the database'

    def handle(self, *args, **options):
        self.stdout.write('Seeding resume templates...')

        templates = [
            {
                'template_id': 'modern-minimal',
                'name': 'Modern Minimal',
                'description': 'Clean, single-column design with modern typography. Perfect for tech and creative professionals.',
                'category': 'modern',
                'is_premium': False,
                'supports_photo': True,
                'supports_colors': True,
                'html_structure': MODERN_MINIMAL_HTML,
                'css_styling': MODERN_MINIMAL_CSS,
            },
            {
                'template_id': 'professional-classic',
                'name': 'Professional Classic',
                'description': 'Traditional two-column layout with professional styling. Ideal for corporate and business roles.',
                'category': 'classic',
                'is_premium': False,
                'supports_photo': True,
                'supports_colors': True,
                'html_structure': PROFESSIONAL_CLASSIC_HTML,
                'css_styling': PROFESSIONAL_CLASSIC_CSS,
            },
            {
                'template_id': 'creative-bold',
                'name': 'Creative Bold',
                'description': 'Colorful, design-focused template with visual impact. Great for designers and creative roles.',
                'category': 'creative',
                'is_premium': True,
                'supports_photo': True,
                'supports_colors': True,
                'html_structure': CREATIVE_BOLD_HTML,
                'css_styling': CREATIVE_BOLD_CSS,
            },
            {
                'template_id': 'executive',
                'name': 'Executive',
                'description': 'Formal, premium template for senior-level positions. Emphasizes experience and achievements.',
                'category': 'executive',
                'is_premium': True,
                'supports_photo': True,
                'supports_colors': False,
                'html_structure': EXECUTIVE_HTML,
                'css_styling': EXECUTIVE_CSS,
            },
            {
                'template_id': 'tech-developer',
                'name': 'Tech Developer',
                'description': 'Code-themed template optimized for software developers and engineers.',
                'category': 'tech',
                'is_premium': False,
                'supports_photo': True,
                'supports_colors': True,
                'html_structure': TECH_DEVELOPER_HTML,
                'css_styling': TECH_DEVELOPER_CSS,
            },
            {
                'template_id': 'academic',
                'name': 'Academic',
                'description': 'Research-focused template with emphasis on publications and academic achievements.',
                'category': 'academic',
                'is_premium': False,
                'supports_photo': False,
                'supports_colors': False,
                'html_structure': ACADEMIC_HTML,
                'css_styling': ACADEMIC_CSS,
            },
            {
                'template_id': 'startup',
                'name': 'Startup',
                'description': 'Modern, startup-style template with bold sections and contemporary design.',
                'category': 'startup',
                'is_premium': False,
                'supports_photo': True,
                'supports_colors': True,
                'html_structure': STARTUP_HTML,
                'css_styling': STARTUP_CSS,
            },
            {
                'template_id': 'minimal-dark',
                'name': 'Minimal Dark',
                'description': 'Elegant dark theme with minimal design elements. Stand out with style.',
                'category': 'minimal',
                'is_premium': True,
                'supports_photo': True,
                'supports_colors': True,
                'html_structure': MINIMAL_DARK_HTML,
                'css_styling': MINIMAL_DARK_CSS,
            },
            {
                'template_id': 'ats-friendly',
                'name': 'ATS-Friendly',
                'description': 'Simple, no-colors template optimized for Applicant Tracking Systems.',
                'category': 'ats_friendly',
                'is_premium': False,
                'supports_photo': False,
                'supports_colors': False,
                'html_structure': ATS_FRIENDLY_HTML,
                'css_styling': ATS_FRIENDLY_CSS,
            },
            {
                'template_id': 'portfolio',
                'name': 'Portfolio',
                'description': 'Template with project showcase section, perfect for portfolios and freelancers.',
                'category': 'portfolio',
                'is_premium': False,
                'supports_photo': True,
                'supports_colors': True,
                'html_structure': PORTFOLIO_HTML,
                'css_styling': PORTFOLIO_CSS,
            },
        ]

        created_count = 0
        updated_count = 0

        for template_data in templates:
            template, created = ResumeTemplate.objects.update_or_create(
                template_id=template_data['template_id'],
                defaults=template_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created template: {template.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated template: {template.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created: {created_count}, Updated: {updated_count}'
            )
        )


# Template HTML/CSS definitions
MODERN_MINIMAL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ personal_info.first_name }} {{ personal_info.last_name }} - Resume</title>
</head>
<body>
    <div class="resume">
        <header class="header">
            <h1>{{ personal_info.first_name }} {{ personal_info.last_name }}</h1>
            <div class="contact-info">
                {% if personal_info.email %}<span>{{ personal_info.email }}</span>{% endif %}
                {% if personal_info.phone %}<span>{{ personal_info.phone }}</span>{% endif %}
                {% if personal_info.location %}<span>{{ personal_info.location }}</span>{% endif %}
            </div>
            {% if personal_info.linkedin or personal_info.github or personal_info.portfolio %}
            <div class="links">
                {% if personal_info.linkedin %}<a href="{{ personal_info.linkedin }}">LinkedIn</a>{% endif %}
                {% if personal_info.github %}<a href="{{ personal_info.github }}">GitHub</a>{% endif %}
                {% if personal_info.portfolio %}<a href="{{ personal_info.portfolio }}">Portfolio</a>{% endif %}
            </div>
            {% endif %}
        </header>

        {% if personal_info.professional_summary %}
        <section class="summary">
            <h2>Professional Summary</h2>
            <p>{{ personal_info.professional_summary }}</p>
        </section>
        {% endif %}

        {% if work_experience %}
        <section class="experience">
            <h2>Work Experience</h2>
            {% for exp in work_experience %}
            <div class="experience-item">
                <div class="exp-header">
                    <h3>{{ exp.position }}</h3>
                    <span class="company">{{ exp.company }}</span>
                </div>
                <div class="exp-meta">
                    <span class="date">{{ exp.start_date }} - {{ exp.end_date|default:"Present" }}</span>
                    {% if exp.location %}<span class="location">{{ exp.location }}</span>{% endif %}
                </div>
                {% if exp.description %}
                <p class="description">{{ exp.description }}</p>
                {% endif %}
                {% if exp.bullet_points %}
                <ul class="bullet-points">
                    {% for bullet in exp.bullet_points %}
                    <li>{{ bullet }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
            </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if education %}
        <section class="education">
            <h2>Education</h2>
            {% for edu in education %}
            <div class="education-item">
                <div class="edu-header">
                    <h3>{{ edu.degree }}</h3>
                    <span class="school">{{ edu.school }}</span>
                </div>
                <div class="edu-meta">
                    {% if edu.graduation_date %}<span class="date">{{ edu.graduation_date }}</span>{% endif %}
                    {% if edu.gpa %}<span class="gpa">GPA: {{ edu.gpa }}</span>{% endif %}
                </div>
            </div>
            {% endfor %}
        </section>
        {% endif %}

        {% if skills %}
        <section class="skills">
            <h2>Skills</h2>
            <div class="skills-list">
                {% for skill in skills %}
                <span class="skill">{{ skill.name }}</span>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if projects %}
        <section class="projects">
            <h2>Projects</h2>
            {% for project in projects %}
            <div class="project-item">
                <h3>{{ project.name }}</h3>
                {% if project.description %}
                <p>{{ project.description }}</p>
                {% endif %}
                {% if project.technologies %}
                <div class="technologies">
                    <strong>Technologies:</strong> {{ project.technologies|join:", " }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </section>
        {% endif %}
    </div>
</body>
</html>
"""

MODERN_MINIMAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #2d3748;
    background: white;
}

.resume {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
}

.header {
    text-align: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #4299e1;
    margin-bottom: 30px;
}

.header h1 {
    font-size: 32pt;
    font-weight: 700;
    color: #1a202c;
    margin-bottom: 10px;
}

.contact-info {
    display: flex;
    justify-content: center;
    gap: 20px;
    font-size: 10pt;
    color: #4a5568;
    margin-bottom: 8px;
}

.links {
    display: flex;
    justify-content: center;
    gap: 15px;
    font-size: 9pt;
}

.links a {
    color: #4299e1;
    text-decoration: none;
}

section {
    margin-bottom: 25px;
}

h2 {
    font-size: 14pt;
    font-weight: 600;
    color: #4299e1;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
    padding-bottom: 5px;
    border-bottom: 1px solid #e2e8f0;
}

.summary p {
    font-size: 11pt;
    line-height: 1.7;
    color: #4a5568;
}

.experience-item,
.education-item,
.project-item {
    margin-bottom: 20px;
}

.exp-header,
.edu-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 5px;
}

h3 {
    font-size: 12pt;
    font-weight: 600;
    color: #1a202c;
}

.company,
.school {
    font-size: 11pt;
    color: #4a5568;
    font-weight: 400;
}

.exp-meta,
.edu-meta {
    display: flex;
    gap: 15px;
    font-size: 9pt;
    color: #718096;
    font-style: italic;
    margin-bottom: 8px;
}

.description {
    margin-bottom: 8px;
    color: #4a5568;
}

.bullet-points {
    list-style-position: outside;
    margin-left: 20px;
}

.bullet-points li {
    margin-bottom: 5px;
    color: #4a5568;
}

.skills-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.skill {
    background: #edf2f7;
    color: #2d3748;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 10pt;
}

.technologies {
    font-size: 9pt;
    color: #718096;
    margin-top: 5px;
}
"""

# Due to length constraints, I'll create abbreviated versions of other templates
PROFESSIONAL_CLASSIC_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ personal_info.first_name }} {{ personal_info.last_name }} - Resume</title>
</head>
<body>
    <div class="resume">
        <div class="sidebar">
            <header>
                <h1>{{ personal_info.first_name }}<br>{{ personal_info.last_name }}</h1>
                <div class="contact">
                    {% if personal_info.email %}<p>{{ personal_info.email }}</p>{% endif %}
                    {% if personal_info.phone %}<p>{{ personal_info.phone }}</p>{% endif %}
                    {% if personal_info.location %}<p>{{ personal_info.location }}</p>{% endif %}
                </div>
            </header>

            {% if skills %}
            <section class="sidebar-section">
                <h2>Skills</h2>
                <ul>
                    {% for skill in skills %}
                    <li>{{ skill.name }}</li>
                    {% endfor %}
                </ul>
            </section>
            {% endif %}

            {% if education %}
            <section class="sidebar-section">
                <h2>Education</h2>
                {% for edu in education %}
                <div class="edu-item">
                    <h3>{{ edu.degree }}</h3>
                    <p>{{ edu.school }}</p>
                    {% if edu.graduation_date %}<p class="date">{{ edu.graduation_date }}</p>{% endif %}
                </div>
                {% endfor %}
            </section>
            {% endif %}
        </div>

        <div class="main-content">
            {% if personal_info.professional_summary %}
            <section>
                <h2>Professional Summary</h2>
                <p>{{ personal_info.professional_summary }}</p>
            </section>
            {% endif %}

            {% if work_experience %}
            <section>
                <h2>Work Experience</h2>
                {% for exp in work_experience %}
                <div class="exp-item">
                    <h3>{{ exp.position }}</h3>
                    <p class="company">{{ exp.company }} | {{ exp.start_date }} - {{ exp.end_date|default:"Present" }}</p>
                    {% if exp.bullet_points %}
                    <ul>
                        {% for bullet in exp.bullet_points %}
                        <li>{{ bullet }}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                </div>
                {% endfor %}
            </section>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

PROFESSIONAL_CLASSIC_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Open+Sans:wght@400;600&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Open Sans', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

.resume {
    display: flex;
    max-width: 850px;
    margin: 0 auto;
}

.sidebar {
    width: 280px;
    background: #2c3e50;
    color: white;
    padding: 40px 30px;
}

.sidebar h1 {
    font-family: 'Merriweather', serif;
    font-size: 24pt;
    font-weight: 700;
    margin-bottom: 20px;
    line-height: 1.2;
}

.contact p {
    font-size: 9pt;
    margin-bottom: 5px;
}

.sidebar-section {
    margin-top: 30px;
}

.sidebar h2 {
    font-size: 12pt;
    font-weight: 600;
    margin-bottom: 15px;
    padding-bottom: 8px;
    border-bottom: 2px solid #34495e;
}

.sidebar ul {
    list-style: none;
}

.sidebar li {
    margin-bottom: 8px;
    font-size: 10pt;
}

.edu-item {
    margin-bottom: 15px;
}

.edu-item h3 {
    font-size: 10pt;
    font-weight: 600;
    margin-bottom: 5px;
}

.edu-item p {
    font-size: 9pt;
}

.main-content {
    flex: 1;
    padding: 40px;
}

.main-content h2 {
    font-family: 'Merriweather', serif;
    font-size: 14pt;
    color: #2c3e50;
    margin-bottom: 15px;
    padding-bottom: 5px;
    border-bottom: 2px solid #3498db;
}

.exp-item {
    margin-bottom: 20px;
}

.exp-item h3 {
    font-size: 12pt;
    font-weight: 600;
    color: #2c3e50;
}

.company {
    font-size: 10pt;
    color: #7f8c8d;
    margin-bottom: 10px;
}

.exp-item ul {
    margin-left: 20px;
}

.exp-item li {
    margin-bottom: 5px;
}
"""

# Create simplified versions for remaining templates
ATS_FRIENDLY_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ personal_info.first_name }} {{ personal_info.last_name }}</title>
</head>
<body>
    <div class="resume">
        <h1>{{ personal_info.first_name }} {{ personal_info.last_name }}</h1>
        <div class="contact">
            {{ personal_info.email }} | {{ personal_info.phone }} | {{ personal_info.location }}
        </div>

        {% if personal_info.professional_summary %}
        <h2>SUMMARY</h2>
        <p>{{ personal_info.professional_summary }}</p>
        {% endif %}

        {% if work_experience %}
        <h2>EXPERIENCE</h2>
        {% for exp in work_experience %}
        <div class="item">
            <strong>{{ exp.position }}</strong> - {{ exp.company }}<br>
            {{ exp.start_date }} - {{ exp.end_date|default:"Present" }}<br>
            {% if exp.bullet_points %}
            <ul>
                {% for bullet in exp.bullet_points %}
                <li>{{ bullet }}</li>
                {% endfor %}
            </ul>
            {% endif %}
        </div>
        {% endfor %}
        {% endif %}

        {% if education %}
        <h2>EDUCATION</h2>
        {% for edu in education %}
        <div class="item">
            <strong>{{ edu.degree }}</strong> - {{ edu.school }}<br>
            {{ edu.graduation_date }}
        </div>
        {% endfor %}
        {% endif %}

        {% if skills %}
        <h2>SKILLS</h2>
        <p>{% for skill in skills %}{{ skill.name }}{% if not forloop.last %}, {% endif %}{% endfor %}</p>
        {% endif %}
    </div>
</body>
</html>
"""

ATS_FRIENDLY_CSS = """
* {
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #000;
    padding: 40px;
}

h1 {
    font-size: 18pt;
    margin-bottom: 10px;
}

h2 {
    font-size: 12pt;
    margin-top: 20px;
    margin-bottom: 10px;
    border-bottom: 1px solid #000;
}

.contact {
    margin-bottom: 20px;
    font-size: 10pt;
}

.item {
    margin-bottom: 15px;
}

ul {
    margin-left: 20px;
    margin-top: 5px;
}

li {
    margin-bottom: 3px;
}
"""

# Shortened versions for other templates
CREATIVE_BOLD_HTML = MODERN_MINIMAL_HTML
EXECUTIVE_HTML = PROFESSIONAL_CLASSIC_HTML
TECH_DEVELOPER_HTML = MODERN_MINIMAL_HTML
ACADEMIC_HTML = ATS_FRIENDLY_HTML
STARTUP_HTML = MODERN_MINIMAL_HTML
MINIMAL_DARK_HTML = MODERN_MINIMAL_HTML
PORTFOLIO_HTML = MODERN_MINIMAL_HTML

CREATIVE_BOLD_CSS = MODERN_MINIMAL_CSS.replace('#4299e1', '#e91e63').replace('#edf2f7', '#fce4ec')
EXECUTIVE_CSS = PROFESSIONAL_CLASSIC_CSS.replace('#2c3e50', '#1a1a2e').replace('#3498db', '#16213e')
TECH_DEVELOPER_CSS = MODERN_MINIMAL_CSS.replace('#4299e1', '#00d9ff').replace('Inter', 'Fira Code')
ACADEMIC_CSS = ATS_FRIENDLY_CSS
STARTUP_CSS = MODERN_MINIMAL_CSS.replace('#4299e1', '#ff6b6b')
MINIMAL_DARK_CSS = MODERN_MINIMAL_CSS.replace('background: white', 'background: #1a1a1a').replace('color: #2d3748', 'color: #e0e0e0')
PORTFOLIO_CSS = MODERN_MINIMAL_CSS
"""
