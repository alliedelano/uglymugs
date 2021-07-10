from django.contrib import admin

# Register your models here.

from .models import Mug, Use, Instruction, Photo
admin.site.register(Mug)
admin.site.register(Use)
admin.site.register(Instruction)
admin.site.register(Photo)
