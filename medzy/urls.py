from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('settings.urls')),
    path('api/', include('dashboard.urls')), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint for obtaining the token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint for refreshing the token
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/prescriptions/', include('prescriptions.urls')),  
    path('api/coupons/', include('coupons.urls')),  
    path('api/notifications/', include('notifications.urls')),
    path('api/ai_assistant/', include('ai_assistant.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)