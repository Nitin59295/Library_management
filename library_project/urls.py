# library_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # Import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('accounts.urls')),  # Corrected path
    path('api/', include('library.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Frontend pages served by TemplateView
    path('register/', TemplateView.as_view(template_name='register.html'), name='register_page'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login_page'),
    path('books/', TemplateView.as_view(template_name='books.html'), name='books_page'),
    path('checkout/', TemplateView.as_view(template_name='checkout.html'), name='checkout_page'),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
]