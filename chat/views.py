from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from web.models import *

from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseNotAllowed

User = get_user_model()

@login_required(login_url='signin')
def join_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    room.participants.add(request.user)
    return JsonResponse({"message": f"Joined room {room.name}"})

@login_required(login_url='signin')
def get_rooms(request):
    rooms = ChatRoom.objects.all().values("id", "name", "created_by__username")
    return JsonResponse(list(rooms), safe=False)

@login_required(login_url='signin')
def get_messages(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    
    if request.user not in room.participants.all():
        return JsonResponse({"error": "You are not a member of this room"}, status=403)

    messages = Message.objects.filter(room=room).order_by("timestamp").values("sender__username", "content", "timestamp")
    return JsonResponse(list(messages), safe=False)

@login_required(login_url='signin')
def room_selection(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    rooms = ChatRoom.objects.all().order_by('-id')  # Fetch all chat rooms
    
    context = {
        'notification': notification,
        'notificationcount': notificationcount,
        
        "rooms": rooms,
    }
    return render(request, "chat/room_list.html", context)

@login_required(login_url='signin')
def chat_room(request, unique_code):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    # Fetch the chat room
    room = get_object_or_404(ChatRoom, unique_code=unique_code)

    # Get all messages for this room
    messages = Message.objects.filter(room=room).order_by('timestamp')
    
    context = {
        'notification': notification,
        'notificationcount': notificationcount,
        
        "unique_code": unique_code,
        "messages": messages,
    }
    # Render the chat room page with messages
    return render(request, "chat/chat_room.html", context)

User = get_user_model()
@login_required(login_url='signin')
def create_room(request):
    # Order the notifications by the most recent ones first
    notification = Notification.objects.filter(user=request.user).order_by('-id')
    notificationcount = Notification.objects.filter(user=request.user, viewed=False).count()
    
    if request.method == "POST":
        room_name = request.POST.get("room_name").strip()

        # Create the chat room with the logged-in user as the creator
        room = ChatRoom.objects.create(name=room_name, status="Active", created_by=request.user)

        # Get or create the "Worntech Support" user (system bot)
        worntech_user, created = User.objects.get_or_create(username="Worntech Support", defaults={"first_name": "Worntech", "last_name": "Support"})

        # Create an initial welcome message in the newly created room
        Message.objects.create(
            room=room,  
            content="Welcome to Worntech Online Customer Care Live Chat! What can we help you? Feel free to ask anything. This is assistant from Worntech online customer care.",
            sender=worntech_user  # ✅ Now uses the actual User instance
        )
        
        context = {
        'notification': notification,
        'notificationcount': notificationcount,
    }
        # Redirect to the chat room using its unique code
        return redirect("chat_room", unique_code=room.unique_code)
    
    return render(request, "chat/create_room.html", context)
    
@login_required(login_url='signin')
def update_chat_status(request, id, status):
    chat = get_object_or_404(ChatRoom, id=id)
    
    # Update the status based on the passed parameter
    if status in ['Active', 'Inactive']:
        chat.status = status
        chat.save()

    return redirect('room_selection')  # Redirect back to the payment view

# @login_required(login_url='signin')
# def deletechat(request, pk):
#     chatdelete = get_object_or_404(ChatRoom, pk=pk)
#     if request.method == "POST":
#         chatdelete.delete()
#         messages.success(request, "Chat deleted successfully.")
#         return redirect('room_selection')
#     return redirect('room_selection')

@csrf_protect
@login_required(login_url='signin')
def deletechat(request, pk):
    chat_room = get_object_or_404(ChatRoom, pk=pk)
    
    if request.method == "POST":
        chat_room.delete()
        messages.success(request, "Chat deleted successfully.")
        return redirect('room_selection')

    # If method is not POST, return a 405 Method Not Allowed response
    return HttpResponseNotAllowed(["POST"])

