from django.urls import path
from .views import home, tracking


urlpatterns = [    
    path("", home, name="home"),
    path("tracking/", home, name="only_tracking"),
    path("tracking/<str:tracking_number>", tracking, name="tracking_page"),    
]
