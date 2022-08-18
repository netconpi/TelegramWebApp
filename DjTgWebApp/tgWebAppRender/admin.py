from django.contrib import admin
from .models import *

admin.site.register(Company)
admin.site.register(Notification)
admin.site.register(Event)
admin.site.register(TelegramData)
admin.site.register(Tag)
admin.site.register(UserApp)



# Register your models here.
