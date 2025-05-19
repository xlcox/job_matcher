from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include('jobs.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'),
         name='dashboard'),
    path('login/', TemplateView.as_view(template_name='login.html'),
         name='login'),
]
