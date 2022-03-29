from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('tasks/view', views.view_tasks),
    path('tasks/create', views.create_task),
    path('tasks/<int:id>/update', views.update_task_by_id, name='id'),
    path('tasks/delete/<int:id>', views.delete_task_by_id, name='id'),

    path('contacts/view', views.view_contacts),
    path('contacts/add', views.add_contact),

    path('msg/create', views.create_msg),
    path('msg/view', views.view_msg),
    path('msg/delete/<int:id>', views.delete_msg_by_id, name='id'),

    path('noti/delete/<int:id>', views.delete_noti_by_id, name='id'),

    path('profile/update/<int:id>', views.update_profile, name='id'),
]