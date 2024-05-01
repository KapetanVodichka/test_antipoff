from django.urls import path
from .views import SimulateExternalServerView

app_name = 'out_service'
urlpatterns = [
    path('simulate/', SimulateExternalServerView.as_view(), name='simulate'),
]