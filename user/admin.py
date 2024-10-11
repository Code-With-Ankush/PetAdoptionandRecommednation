from django.contrib import admin
from .models import Map_Details, Dog_Pics

# Custom admin class for Dog_Pics to display additional fields in the admin list view
class DogPicsAdmin(admin.ModelAdmin):
    list_display = (
        'map_id', 'pet_name', 'pet_breed', 'pet_age', 'pet_status', 
        'pet_gender', 'pet_size', 'pet_color', 'health_status', 
        'vaccinated', 'spayed_neutered', 'status', 'uploaded_at'
    )
    search_fields = ('pet_name', 'pet_breed', 'map_id__place_name')
    list_filter = ('pet_status', 'pet_gender', 'vaccinated', 'spayed_neutered', 'status')
    readonly_fields = ('uploaded_at',)

# Custom admin class for Map_Details to display additional fields in the admin list view
class MapDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'email', 'place_name', 'no_of_dogs', 'behaviour', 
        'zone', 'radius_color', 'latitude', 'longitude', 'km_distance', 'datetime'
    )
    search_fields = ('place_name', 'user__username', 'behaviour')
    list_filter = ('zone', 'km_distance')
    readonly_fields = ('datetime',)

# Registering the models and admin classes with Django admin
admin.site.register(Dog_Pics, DogPicsAdmin)
admin.site.register(Map_Details, MapDetailsAdmin)
