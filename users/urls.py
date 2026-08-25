from django.urls import path
from .views import ProfileRetrieveUpdateAPIView

app_name = "users"

urlpatterns = [
    path("profile/", ProfileRetrieveUpdateAPIView.as_view(), name="profile"),
]