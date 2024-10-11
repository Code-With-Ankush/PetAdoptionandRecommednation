from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpRequest
from user.models import Map_Details, Dog_Pics
from accounts.models import User
import geocoder
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Dashboard view
def dashboard(request):
    user_count = User.objects.exclude(role='admin').count()
    context = {'user_count': user_count}
    return render(request, 'user/dashboard.html', context)

# View all dogspot markers on the map with pet details
def map_view(request):
    latlng = geocoder.ip('me')
    map_db = Map_Details.objects.all()
    
    # Include pet details in the context
    pet_data = Dog_Pics.objects.all()
    context = {
        'lat': latlng.lat, 
        'lng': latlng.lng, 
        'map_db': map_db,
        'pet_data': pet_data
    }
    return render(request, 'user/map_view.html', context)

# View static map of dogspot markers with pet details
def static_dogspot_marker_map(request):
    latlng = geocoder.ip('me')
    map_db = Map_Details.objects.all()
    pet_data = Dog_Pics.objects.all()
    context = {
        'lat': latlng.lat, 
        'lng': latlng.lng, 
        'map_db': map_db,
        'pet_data': pet_data
    }
    return render(request, 'user/static_dogspot_marker_map.html', context)

# Image compression utility function
def image_compressor(image_file, quality=90):
    img = Image.open(image_file)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG', quality=quality)
    img_bytes.seek(0)
    compressed_image = ContentFile(img_bytes.read(), name=image_file.name)
    return compressed_image

from django.http import JsonResponse
from django.shortcuts import render
from .models import Map_Details, Dog_Pics
import os

# View for adding a dogspot
def add_dogspot(request, lat, lng):
    if request.method == 'POST':
        # Get form data
        place_name = request.POST.get('place_name')
        description = request.POST.get('description')
        no_of_dogs = request.POST.get('no_of_dogs')
        behaviour = request.POST.get('behaviour')
        km = request.POST.get('km')

        # Pet details
        pet_name = request.POST.get('pet_name')
        pet_breed = request.POST.get('pet_breed')
        pet_age = request.POST.get('pet_age')
        pet_gender = request.POST.get('pet_gender')
        pet_size = request.POST.get('pet_size')
        pet_color = request.POST.get('pet_color')
        health_status = request.POST.get('health_status')
        vaccinated = request.POST.get('vaccinated') == 'True'
        spayed_neutered = request.POST.get('spayed_neutered') == 'True'

        # Check if the dogspot for the given lat/lng already exists
        if Map_Details.objects.filter(latitude=lat, longitude=lng).exists():
            return JsonResponse({'point_exist': True})

        # Save the dogspot
        map_obj = Map_Details.objects.create(
            user=request.user,
            email=request.user.email,
            place_name=place_name,
            description=description,
            no_of_dogs=no_of_dogs,
            behaviour=behaviour,
            longitude=lng,
            latitude=lat,
            km_distance=km
        )

        # Process the images and pet details
        for i in range(0, int(request.POST.get('length'))):
            image = request.FILES.get(f'images{i}')

            Dog_Pics.objects.create(
                map_id=map_obj,
                image=image,
                pet_name=pet_name,
                pet_breed=pet_breed,
                pet_age=pet_age,
                pet_gender=pet_gender,
                pet_size=pet_size,
                pet_color=pet_color,
                health_status=health_status,
                vaccinated=vaccinated,
                spayed_neutered=spayed_neutered
            )

        # Return success response
        return JsonResponse({'success': True})

    return render(request, 'user/add_dogspot.html', {'lat': lat, 'lng': lng})


# List all dogspots with pet details for a user
def dogspot_list(request):
    map_data = Map_Details.objects.filter(user=request.user.id)
    pet_data = Dog_Pics.objects.filter(map_id__user=request.user.id)
    context = {'map_data': map_data, 'pet_data': pet_data}
    return render(request, 'user/dogspot_list.html', context)

# Update a dogspot with pet details
def dogspot_update(request):
    if request.method == 'POST' and not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        object_id = request.POST.get('id')

        if Map_Details.objects.filter(user=request.user.id, id=object_id).exists():
            single_map_object = Map_Details.objects.filter(user=request.user.id, id=object_id).first()
            context = {'single_map_object': single_map_object}
            return render(request, 'user/dogspot_update.html', context)

    elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
        object_id = request.POST.get('id')
        length = request.POST.get('length')
        place_name = request.POST.get('place_name')
        description = request.POST.get('description')
        no_of_dogs = request.POST.get('no_of_dogs')
        behaviour = request.POST.get('behaviour')
        km = request.POST.get('km')

        # Pet details
        pet_name = request.POST.get('pet_name', 'Unknown Pet')
        pet_breed = request.POST.get('pet_breed', 'Unknown Breed')
        pet_age = request.POST.get('pet_age', 0)
        pet_status = request.POST.get('pet_status', 'Available')
        pet_gender = request.POST.get('pet_gender', 'Male')
        pet_size = request.POST.get('pet_size', 'Medium')
        pet_color = request.POST.get('pet_color', 'Unknown')
        health_status = request.POST.get('health_status', 'Healthy')
        vaccinated = request.POST.get('vaccinated', False)
        spayed_neutered = request.POST.get('spayed_neutered', False)

        if Map_Details.objects.filter(user=request.user.id, id=object_id).exists():
            map_object = Map_Details.objects.get(user=request.user.id, id=object_id)

            # Zone determination based on behaviour
            zone = {}
            if 'Aggressive' in behaviour or 'Biting' in behaviour or 'Territorial' in behaviour or 'Illness' in behaviour:
                zone = {'zone': 'red', 'radius_color': '#FF0000', 'radius_color_hexcode': '#FF0000'}
            elif 'Barking' in behaviour or 'Chasing' in behaviour:
                zone = {'zone': 'yellow', 'radius_color': '#FFD326', 'radius_color_hexcode': '#FFD326'}
            else:
                zone = {'zone': 'green', 'radius_color': '#2AAD27', 'radius_color_hexcode': '#2AAD27'}

            # Update the map details
            map_object.place_name = place_name
            map_object.description = description
            map_object.no_of_dogs = no_of_dogs
            map_object.behaviour = behaviour
            map_object.zone = zone['zone']
            map_object.radius_color = zone['radius_color']
            map_object.radius_color_hexcode = zone['radius_color_hexcode']
            map_object.km_distance = km
            map_object.save()

            # Handle image and pet detail updates
            dog_pics_db = map_object.dog_pics.all()
            dog_pics_db_images_length = dog_pics_db.count()

            if dog_pics_db_images_length != int(length):
                for dog_pics_row in map_object.dog_pics.all():
                    if dog_pics_row.image and os.path.exists(dog_pics_row.image.path):
                        os.remove(dog_pics_row.image.path)
                dog_pics_db.delete()

                # Add new images and pet details
                for file_num in range(0, int(length)):
                    image = request.FILES.get(f'images{file_num}')
                    Dog_Pics.objects.create(
                        map_id=map_object,
                        image=image_compressor(image),
                        pet_name=pet_name,
                        pet_breed=pet_breed,
                        pet_age=pet_age,
                        pet_status=pet_status,
                        pet_gender=pet_gender,
                        pet_size=pet_size,
                        pet_color=pet_color,
                        health_status=health_status,
                        vaccinated=vaccinated,
                        spayed_neutered=spayed_neutered
                    )

            return JsonResponse({'status': True}, safe=False)

    else:
        return redirect(dogspot_list)

# Delete a dogspot and associated pet details
def dogspot_delete(request):
    if request.method == 'POST':
        object_id = request.POST.get('delete_id')
        if Map_Details.objects.filter(user=request.user.id, id=object_id).exists():
            map_object = Map_Details.objects.get(user=request.user.id, id=object_id)

            # Delete images from the file system
            for dog_pics_row in map_object.dog_pics.all():
                if dog_pics_row.image and os.path.exists(dog_pics_row.image.path):
                    os.remove(dog_pics_row.image.path)

            map_object.dog_pics.all().delete()  # Delete related images and pet details from the database
            map_object.delete()  # Delete the map details entry
            messages.success(request, map_object.place_name, extra_tags='delete_msg')
            return redirect('user.dogspot_list')
    
    return redirect('user.dashboard')

# View all dogspots with pet details
def all_dogspot_list(request):
    map_data = Map_Details.objects.all()
    pet_data = Dog_Pics.objects.all()
    context = {'map_data': map_data, 'pet_data': pet_data}
    return render(request, 'user/all_dogspot_list.html', context)

# User profile
def profile(request):
    return render(request, 'user/profile.html')

# Update user profile
def profile_update(request):
    return render(request, 'user/profile_update.html')

# User settings
def settings(request):
    return render(request, 'user/profile.html')
