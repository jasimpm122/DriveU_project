
from django.shortcuts import render
from DriveU_Project.models import process_images, image_urls


def image_metrics_view(request):
    images = process_images(image_urls)
    return render(request, 'images.html', {'metrics': images})
