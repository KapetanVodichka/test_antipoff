from django.urls import path
from .views import QueryView, ResultView, PingView, HistoryView

app_name = 'service'

urlpatterns = [
    path('query/', QueryView.as_view(), name='query'),
    path('result/', ResultView.as_view(), name='result'),
    path('ping/', PingView.as_view(), name='ping'),
    path('history/', HistoryView.as_view(), name='history'),
]