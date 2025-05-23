"""sitempsi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include

urlpatterns = [
    path('adminj/', admin.site.urls),
    path('etudedossier2021/', include('etudedossier2021.urls')),
    path('etudedossier2022/', include('etudedossier2022.urls')),
    path('etudedossier2023/', include('etudedossier2023.urls')),
    path('etudedossier2024/', include('etudedossier2024.urls')),
    path('etudedossier2025/', include('etudedossier2025.urls')),
    path('', include('gestionmenu.urls')),
    path('', include('base.urls')),
]
