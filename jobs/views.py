from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from .authentication import APIKeyAuthentication
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)


@api_view(['POST'])
@authentication_classes([APIKeyAuthentication])
def upsert_job(request):
    """
    API endpoint to create or update a job listing.
    
    Upsert Logic:
    - If job_id exists: Update the existing record
    - If job_id doesn't exist: Create a new record
    
    Request Headers:
        X-API-Key: Your API authentication key
    
    Request Body (JSON):
        {
            "job_id": "12345",
            "title": "Senior Backend Engineer",
            "company": "Tech Corp",
            "location": "San Francisco, CA",
            "description": "We are looking for...",
            "date_scraped": "2024-01-15T10:30:00Z"
        }
    
    Returns:
        201: Job created
        200: Job updated
        400: Invalid data
        401: Authentication failed
    """
    try:
        serializer = JobSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"Validation error: {serializer.errors}")
            return Response(
                {
                    'error': 'Invalid data',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        job_id = serializer.validated_data.get('job_id')
        
        # Perform upsert operation
        job, created = Job.objects.update_or_create(
            job_id=job_id,
            defaults=serializer.validated_data
        )
        
        result_serializer = JobSerializer(job)
        
        if created:
            logger.info(f"Created new job: {job_id}")
            return Response(
                {
                    'message': 'Job created successfully',
                    'data': result_serializer.data,
                    'created': True
                },
                status=status.HTTP_201_CREATED
            )
        else:
            logger.info(f"Updated existing job: {job_id}")
            return Response(
                {
                    'message': 'Job updated successfully',
                    'data': result_serializer.data,
                    'created': False
                },
                status=status.HTTP_200_OK
            )
    
    except Exception as e:
        logger.exception(f"Unexpected error in upsert_job: {str(e)}")
        return Response(
            {
                'error': 'Internal server error',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    Simple health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now()
    })
