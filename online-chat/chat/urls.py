from django.urls import path
from . import views

app_name = 'chat'

# changed "{}" to "[]" and the error was gone. WIERED!!!
urlpatterns = [
    path('api/create-room/<str:uuid>/',views.create_room, name='create-room'),
    path('chat-admin/', views.admin, name='admin'),
    path('chat-admin/add-user/', views.add_user, name='add_user'),
    path('chat-admin/<str:uuid>/',views.room, name='room'),
    path('chat-admin/users/<uuid:uuid>/', views.user_detail, name='user_detail'),
    path('chat-admin/users/<str:uuid>/edit/', views.edit_user, name='edit_user'),
    path('chat-admin/users/<str:uuid>/delete/', views.delete_room, name='delete_room'),

]