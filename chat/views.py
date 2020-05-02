from django.contrib.auth import get_user_model

from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.shortcuts import render
from django.views.generic.base import View

User = get_user_model()

class index(View):
    
    def get(self, request, *args, **kwargs ):
        room_list = Room.objects.order_by('-created_at')[:5]
        context = {
            'room_list': room_list,
        }
        return render( request, 'chat/index.html', context )

class chat(View):
    
    def get(self, request, *args, **kwargs ):
        room_name= kwargs.get('room_name') 
        messages = Message.objects.filter(room__name=room_name).order_by('-created_at')[:50]
        room = Room.objects.filter(name=room_name)[0]
        template = loader.get_template('chat/chat_room.html')
        context = {
            'messages': messages,
            'room': room
        }
        return HttpResponse(template.render(context, request))

class room(View):
    
    def post(self, request, *args, **kwargs ):
        name = request.POST.get("room_name")
        room = Room.objects.create(name=name)
        return HttpResponseRedirect(reverse('chat:chat_room', args=[name]))
