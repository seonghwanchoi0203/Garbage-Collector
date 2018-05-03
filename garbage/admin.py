from django.contrib import admin

from garbage.models import Garbage
from garbage.models import Watch

# Register your models here.
admin.site.register(Garbage)
admin.site.register(Watch)