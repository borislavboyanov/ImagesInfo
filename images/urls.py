from django.contrib import admin
from django.urls import path
from .views import create, check_images, upload_images

urlpatterns = [
    path('', create),
    path('check/<str:url>', check_images),
    path('upload', upload_images)
]
