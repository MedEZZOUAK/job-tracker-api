from rest_framework import viewsets, status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count
from django.http import FileResponse
from .models import Application, ApplicationNote, StatusChange
from .serializers import ApplicationSerializer, ApplicationNoteSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filtering and searching configuration
    filterset_fields = ['status']
    search_fields = ['company', 'role']
    ordering_fields = ['applied_at', 'updated_at']
    ordering = ['-applied_at']

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Application.objects.none()
            
        # Users can only see and edit their own applications, unless they are admins
        if self.request.user.groups.filter(name='Admins').exists() or self.request.user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        old_status = instance.status
        new_status = serializer.validated_data.get('status', old_status)
        
        if old_status != new_status:
            StatusChange.objects.create(
                application=instance,
                from_status=old_status,
                to_status=new_status
            )
        
        serializer.save()

    @action(detail=True, methods=['get'])
    def download_resume(self, request, pk=None):
        application = self.get_object()
        if not application.resume:
            return Response({"detail": "No resume found for this application."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            return FileResponse(application.resume.open(), as_attachment=True)
        except FileNotFoundError:
            return Response({"detail": "Resume file not found on server."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        
        total = queryset.count()
        by_status = queryset.values('status').annotate(count=Count('status'))
        
        status_counts = {item['status']: item['count'] for item in by_status}
        for status_key, _ in Application.STATUS_CHOICES:
            if status_key not in status_counts:
                status_counts[status_key] = 0
                
        return Response({
            'total_applications': total,
            'by_status': status_counts
        })

class ApplicationNoteViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ApplicationNote.objects.filter(application__user=self.request.user)

    def perform_create(self, serializer):
        application = serializer.validated_data['application']
        if application.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to add notes to this application.")
        serializer.save()
