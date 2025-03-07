from django.urls import path
from . import views

urlpatterns = [
    path("create-room/", views.create_room, name="create-room"),
    path("join-room/<int:room_id>/", views.join_room, name="join-room"),
    path("get-rooms/", views.get_rooms, name="get-rooms"),
    path("get-messages/<int:room_id>/", views.get_messages, name="get-messages"),
    
    path("room_selection/", views.room_selection, name="room_selection"),
    path("create/", views.create_room, name="create_room"),
    path("chat/<str:unique_code>/", views.chat_room, name="chat_room"),  # ✅ Use unique_code
    
    path('update_chat_status/<int:id>/<str:status>/', views.update_chat_status, name='update_chat_status'),
    
    path('deletechat/<int:pk>/', views.deletechat, name = "deletechat"),
]
