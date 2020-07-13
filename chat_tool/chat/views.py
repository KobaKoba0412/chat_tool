from django.contrib.auth import get_user_model

from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.shortcuts import render
from django.views.generic.base import View

from .forms import CreateRoomForm

User = get_user_model()

class index(generic.CreateView):

    template_name = 'chat/index.html'
    form_class = CreateRoomForm

    def get_context_data(self, **kwargs):
        room_list = Room.objects.order_by('-created_at')[:5]
        kwargs["room_list"] = room_list
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        room = form.save()
        return HttpResponseRedirect(reverse('chat:chat_room', args=[room.name]))

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

