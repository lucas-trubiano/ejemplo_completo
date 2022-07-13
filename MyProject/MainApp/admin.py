from django.contrib import admin

# Register your models here.

from .models import *
from .forms import *

class ModuloAdmin(admin.ModelAdmin):
    form = ModuloAdminForm

class UserAdmin(admin.ModelAdmin):

    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']

class ExtraUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol']
    list_filter = ['rol']
    

admin.site.register(User, UserAdmin)
admin.site.register(ExtraUser, ExtraUserAdmin)

admin.site.register(Categoria)
admin.site.register(Curso)
admin.site.register(Modulo, ModuloAdmin)