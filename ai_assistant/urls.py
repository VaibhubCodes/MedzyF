from django.urls import path
from .views import AIQueryView

urlpatterns = [
    path('process/', AIQueryView.as_view(), name='medzy-ai-process'),
]
