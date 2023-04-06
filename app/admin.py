from django.contrib import admin
from .models import Message,MessageUpdate
# Register your models here.
admin.site.register(Message)
admin.site.register(MessageUpdate)