"""kwadoxi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Site Tops"
admin.site.index_title = "Admin Panel"

urlpatterns = [
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("certificates/", include("certificates.urls")),
    # path("blog/", include("blog.urls")),
    path("cmz/", include("cmz.urls")),
    path("ormed/", include("ormed.urls")),
    path("cecab/", include("cecab.urls")),
    path("fly/", include("fly.urls")),
    path("troca/", include("troca.urls")),
    path("ground/", include("ground.urls")),
    path("boleia/", include("boleia.urls")),
    path("bespoketour/", include("bespoketour.urls")),

    path("setup/", include("setup.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
