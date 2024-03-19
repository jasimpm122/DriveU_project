from DriveU_Project.views import image_metrics_view
from django.urls import path

urlpatterns = [
    path('images/', image_metrics_view)
]
