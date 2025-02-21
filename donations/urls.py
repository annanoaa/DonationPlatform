from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationRequestViewSet

router = DefaultRouter()
router.register(r'requests', DonationRequestViewSet, basename='donationrequest')

urlpatterns = [
    path('', include(router.urls)),
]