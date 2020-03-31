from django.contrib import admin
from .models import CustomUser, WorkPlace, WorkPlacePersonRelation, Channel, direct_message, Channel_message

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(WorkPlace)
admin.site.register(WorkPlacePersonRelation)
admin.site.register(Channel)
admin.site.register(direct_message)
admin.site.register(Channel_message)