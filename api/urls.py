from django.urls import path, include


urlpatterns = [path("", include("api.user.urls")), path("", include("api.vendor.urls"))]
