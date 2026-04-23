from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_home, name="api-home"),
    path('metadata', views.UnifiedMetadataView.as_view(), name="unified-metadata"),
]
