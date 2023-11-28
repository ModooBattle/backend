from django.contrib import admin
from .models import User, MyAddress
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
	("Profile", {
			"fields": ("username",),
			"classes": ("wide",),
		},
	),
	("Permissions",{
			"fields": (
				"is_active",
				"is_staff",
				"is_superuser",
				# "user_permissions",
			),
		},
	),
	("Important Dates", {
			"fields": ("password","last_login", "date_joined", "uuid"),
			"classes": ("collapse",),   #접었다폈다
		},
	),
)
    list_display = ("id","username", "is_superuser", "is_staff", "age",'gender',)
    list_filter = ("is_superuser","is_staff",'age','gender',)
    search_fields = ("username",)
    ordering = ("id",)
    # filter_horizontal = (
    #     "groups",
    #     "user_permissions",
    # )
	
    readonly_fields = ("date_joined", "last_login",)


    
@admin.register(MyAddress)
class MyAddressAdmin(admin.ModelAdmin):  
    list_display = ('id', 'user', 'address', 'latitude', 'longitude',)
    
