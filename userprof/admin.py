from django.contrib import admin
from userprof.models import AdminUser
from userprof.models import ExtendedUser

# Register your models here.
admin.site.register(AdminUser)
admin.site.register(ExtendedUser)
