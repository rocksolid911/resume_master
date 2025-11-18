"""
PDF Generation Service using WeasyPrint
"""
from weasyprint import HTML, CSS
from django.template import Template, Context
from django.conf import settings
from typing import Dict
import logging
import os
from io import BytesIO

logger = logging.getLogger(__name__)


class PDFService:
    """Service for generating PDF resumes"""

    def generate_pdf(self, resume_data: Dict, template_html: str, template_css: str) -> BytesIO:
        """
        Generate PDF from resume data and template

        Args:
            resume_data: Resume data dictionary
            template_html: HTML template string
            template_css: CSS styling string

        Returns:
            BytesIO object containing PDF data
        """
        try:
            # Render HTML with resume data
            html_content = self._render_html(resume_data, template_html)

            # Create PDF
            pdf_buffer = BytesIO()

            HTML(string=html_content).write_pdf(
                pdf_buffer,
                stylesheets=[CSS(string=template_css)],
            )

            pdf_buffer.seek(0)

            logger.info("PDF generated successfully")
            return pdf_buffer

        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            raise

    def _render_html(self, resume_data: Dict, template_html: str) -> str:
        """
        Render HTML template with resume data

        Args:
            resume_data: Resume data dictionary
            template_html: HTML template string

        Returns:
            Rendered HTML string
        """
        # Create Django template
        template = Template(template_html)

        # Create context with resume data
        context = Context({
            'resume': resume_data,
            'personal_info': resume_data.get('personal_info', {}),
            'work_experience': resume_data.get('work_experience', []),
            'education': resume_data.get('education', []),
            'skills': resume_data.get('skills', []),
            'projects': resume_data.get('projects', []),
            'certifications': resume_data.get('certifications', []),
            'languages': resume_data.get('languages', []),
            'awards': resume_data.get('awards', []),
        })

        # Render template
        html_content = template.render(context)

        return html_content

    def save_pdf_file(self, resume, pdf_buffer: BytesIO) -> str:
        """
        Save PDF file to disk/S3 and update resume model

        Args:
            resume: UserResume instance
            pdf_buffer: BytesIO containing PDF data

        Returns:
            File path/URL
        """
        from django.core.files.base import ContentFile

        filename = f"resume_{resume.id}_{resume.user.id}.pdf"

        # Save to model's FileField (will handle S3 if configured)
        resume.pdf_file.save(
            filename,
            ContentFile(pdf_buffer.getvalue()),
            save=True
        )

        logger.info(f"PDF saved: {resume.pdf_file.url}")
        return resume.pdf_file.url
