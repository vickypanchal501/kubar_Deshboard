from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , UserPersonalDetails

# admin.site.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id','username','email','number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2'),
    #     }),
    # )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

class UserPersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ("user", "aadhar_number","pan_number")
admin.site.register(UserPersonalDetails, UserPersonalDetailsAdmin)