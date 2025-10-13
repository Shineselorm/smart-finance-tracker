from django.urls import path
from . import views

urlpatterns = [
    path('', views.insights_dashboard, name='insights_dashboard'),
    path('<int:pk>/read/', views.mark_insight_read, name='mark_insight_read'),
    path('<int:pk>/delete/', views.delete_insight, name='delete_insight'),
]

