from django.urls import path
from .views import PostBackView


urlpatterns = [
    path('postback/<int:event_type>/',
         PostBackView.as_view(), name="postback-view"),
]
