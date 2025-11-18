"""
User Resume Views
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from api.models import UserResume
from api.serializers import (
    UserResumeSerializer,
    UserResumeListSerializer,
    UserResumeCreateSerializer
)
from api.services import PDFService, DOCXService
from api.utils.permissions import IsOwner
import logging

logger = logging.getLogger(__name__)


class UserResumeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user resumes
    GET /api/resumes/ - List user's resumes
    POST /api/resumes/ - Create new resume
    GET /api/resumes/{id}/ - Get resume details
    PUT /api/resumes/{id}/ - Update resume
    DELETE /api/resumes/{id}/ - Delete resume
    GET /api/resumes/{id}/download/ - Download as PDF
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Return resumes for current user"""
        return UserResume.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserResumeListSerializer
        elif self.action == 'create':
            return UserResumeCreateSerializer
        return UserResumeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Filter by active status
        is_active = request.query_params.get('active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'data': {
                'count': queryset.count(),
                'resumes': serializer.data
            }
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save()

        logger.info(f"New resume created: {resume.id} by {request.user.email}")

        return Response({
            'success': True,
            'message': 'Resume created successfully',
            'data': UserResumeSerializer(resume).data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'success': True,
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Invalidate cached PDF/DOCX files when resume is updated
        instance.pdf_file.delete(save=False)
        instance.docx_file.delete(save=False)
        instance.pdf_file = None
        instance.docx_file = None
        instance.save()

        logger.info(f"Resume updated: {instance.id}")

        return Response({
            'success': True,
            'message': 'Resume updated successfully',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        resume_id = instance.id

        # Delete associated files
        if instance.pdf_file:
            instance.pdf_file.delete()
        if instance.docx_file:
            instance.docx_file.delete()

        instance.delete()

        logger.info(f"Resume deleted: {resume_id}")

        return Response({
            'success': True,
            'message': 'Resume deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download resume as PDF or DOCX
        GET /api/resumes/{id}/download/?format=pdf
        """
        resume = self.get_object()
        file_format = request.query_params.get('format', 'pdf').lower()

        try:
            if file_format == 'pdf':
                # Generate PDF
                pdf_service = PDFService()

                # Check if PDF already exists
                if resume.pdf_file:
                    return FileResponse(
                        resume.pdf_file.open('rb'),
                        as_attachment=True,
                        filename=f"resume_{resume.id}.pdf"
                    )

                # Generate new PDF
                pdf_buffer = pdf_service.generate_pdf(
                    resume.resume_data_json,
                    resume.template.html_structure,
                    resume.template.css_styling
                )

                # Save PDF
                pdf_service.save_pdf_file(resume, pdf_buffer)

                # Increment download counter
                resume.increment_download_count()

                # Return PDF
                pdf_buffer.seek(0)
                response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="resume_{resume.id}.pdf"'

                logger.info(f"Resume PDF downloaded: {resume.id}")
                return response

            elif file_format == 'docx':
                # Generate DOCX
                docx_service = DOCXService()

                # Check if DOCX already exists
                if resume.docx_file:
                    return FileResponse(
                        resume.docx_file.open('rb'),
                        as_attachment=True,
                        filename=f"resume_{resume.id}.docx"
                    )

                # Generate new DOCX
                docx_buffer = docx_service.generate_docx(resume.resume_data_json)

                # Save DOCX
                docx_service.save_docx_file(resume, docx_buffer)

                # Increment download counter
                resume.increment_download_count()

                # Return DOCX
                docx_buffer.seek(0)
                response = HttpResponse(
                    docx_buffer.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = f'attachment; filename="resume_{resume.id}.docx"'

                logger.info(f"Resume DOCX downloaded: {resume.id}")
                return response

            else:
                return Response({
                    'success': False,
                    'error': {
                        'message': 'Invalid format. Use pdf or docx',
                        'type': 'ValidationError'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Download failed for resume {resume.id}: {str(e)}")
            return Response({
                'success': False,
                'error': {
                    'message': f'Failed to generate {file_format.upper()}: {str(e)}',
                    'type': 'GenerationError'
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a resume"""
        original_resume = self.get_object()

        # Create a copy
        new_resume = UserResume.objects.create(
            user=original_resume.user,
            template=original_resume.template,
            title=f"{original_resume.title} (Copy)",
            resume_data_json=original_resume.resume_data_json,
            custom_colors=original_resume.custom_colors,
            custom_fonts=original_resume.custom_fonts,
        )

        logger.info(f"Resume duplicated: {original_resume.id} -> {new_resume.id}")

        return Response({
            'success': True,
            'message': 'Resume duplicated successfully',
            'data': UserResumeSerializer(new_resume).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def toggle_public(self, request, pk=None):
        """Toggle resume public visibility"""
        resume = self.get_object()
        resume.is_public = not resume.is_public
        resume.save()

        logger.info(f"Resume visibility toggled: {resume.id} -> {resume.is_public}")

        return Response({
            'success': True,
            'message': f"Resume is now {'public' if resume.is_public else 'private'}",
            'data': {
                'is_public': resume.is_public,
                'public_url': f"/public/{resume.public_slug}" if resume.is_public else None
            }
        })
