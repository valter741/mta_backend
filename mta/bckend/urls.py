from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/view', views.view_tasks),
    path('tasks/create', views.create_task),
    path('tasks/<int:id>/update', views.update_task_by_id, name='id'),
]