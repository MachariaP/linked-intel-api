from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for Job model with validation.
    """
    
    class Meta:
        model = Job
        fields = [
            'id',
            'job_id',
            'title',
            'company',
            'location',
            'description',
            'date_scraped',
            'date_updated',
            'created_at'
        ]
        read_only_fields = ['id', 'date_updated', 'created_at']
    
    def validate_job_id(self, value):
        """
        Ensure job_id is not empty and properly formatted.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("job_id cannot be empty")
        return value.strip()
    
    def validate_title(self, value):
        """
        Validate job title is not empty.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()
