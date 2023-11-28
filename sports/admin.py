from django.contrib import admin
from .models import Sport, Weight, Gym


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):  
    list_display = ('id', 'name',)

    
@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):  
    list_display = ('id', 'sport', 'gender', 'min_weight',)
    list_filter = ('sport', 'gender',)
    
@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):  
    list_display = ('id', 'sport', 'name', 'address', 'latitude', 'longitude')
    list_filter = ('sport',)