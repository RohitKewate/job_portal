from django.urls import path
from . import views

urlpatterns = [
    path('jobs/',views.get_all_jobs,name="get_jobs"),
    path('job/<str:pk>',views.get_job_by_id,name="get_job_by_id"),
    path('create-job/',views.create_job,name="create_job"),
    path('job/<str:pk>/update',views.update_job,name="update_job"),
    path('job/<str:pk>/delete',views.delete_job,name="delete_job"),
    path('stats/<str:topic>/',views.get_topic_stats,name="get_topic_stats"),
]