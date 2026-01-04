from django.urls import path
from .views import upsert_job, health_check

app_name = 'jobs'

urlpatterns = [
    path('api/jobs/upsert/', upsert_job, name='upsert_job'),
    path('api/health/', health_check, name='health_check'),
]
