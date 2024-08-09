from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Interviewer, InterviewTeam

# Register your models here.
class UserAdmin(admin.ModelAdmin):
   list_display = ('email', 'name', 'is_approved', 'is_active', 'is_staff', 'is_superuser')
   list_filter = ('email', 'is_staff', 'is_approved', 'is_active')
   fieldsets = (
      (None, {'fields': ('email', 'name', 'password', 'is_approved', 'is_active',
      'is_staff', 'is_superuser', 'user_permissions')}),
   )
   add_fieldsets = (
      (None, {
         'classes': ('wide', ),
         'fields': ('email', 'name', 'password1', 'password2', 'is_approved', 'is_active')
      }),
   )
   search_fields = ('email', 'name', )
   ordering = ('name', )
   filter_horizontal = ('user_permissions', )

admin.site.register(Interviewer, UserAdmin)
admin.site.register(InterviewTeam)