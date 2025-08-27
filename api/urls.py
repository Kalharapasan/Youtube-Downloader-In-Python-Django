from django.urls import path
from . import views

urlpatterns = [
    path('', views.downloader_ui, name='downloader_ui'),
    path("download/ytdlp", views.download_video, name="download_video"),
    path("video-info", views.video_info, name="video_info"),
]
