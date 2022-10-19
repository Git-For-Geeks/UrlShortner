from django.contrib import admin

from .models import LongToShort, Meta_Data
# Register your models here.
admin.site.register(LongToShort)
admin.site.register(Meta_Data)
