"""eup_coder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from backend import views

urlpatterns = [
    # HTML Page
    path('', views.index, name='home'),
    path('code-builder/', views.code_builder, name='code-builder'),
    path('code-builder/refresh/', views.refresh_cache, name='refresh-cache'),
    path('kind-coefficient-settings/', views.kind_coefficient_settings, name='kind-coefficient-settings'),
    path('kind-coefficient-settings/refresh/', views.kind_coefficient_settings_refresh, name='kind-coefficient-settings-refresh'),

    # 인증
    path('auth/login/', auth_views.LoginView.as_view(), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # API
    path('api/v1/modifier-info/', views.code_builder_json, name='code-builder-json'),
    path('api/v1/modifier-info/update-point/', views.update_point, name='update-point'),
    path('api/v1/kind-coefficient-settings/', views.kind_coefficient_settings_json, name='kind-coefficient-settings-json'),
    path('api/v1/kind-coefficient-settings/update-point/', views.update_kind_point, name='update-kind-point'),
    path('api/v1/built-code/', views.get_built_data, name='built-code')
]
