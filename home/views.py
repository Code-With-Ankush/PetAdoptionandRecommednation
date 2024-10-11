from django.shortcuts import render

import geocoder

from user.models import Map_Details
# Create your views here.

# index
def index(request):
    latlng = geocoder.ip('me')
    # if request.user.is_authenticated: 
    #     print(request.user,'User already logged in')
    #     return render(request,'admin/dashboard.html')
    # else:
    print(latlng)
    print(latlng.ip)
    print(latlng.lat)
    print(latlng.lng)

    map_db = Map_Details.objects.all()
    return render(request,'home/home.html',{'lat':latlng.lat, 'lng':latlng.lng, 'map_db': map_db})

from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home.index')  # Success redirect
    else:
        form = ContactForm()

    return render(request, 'home/contact_us.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Pet

def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    context = {
        'pet': pet
    }
    return render(request, 'user/pet_detail.html', context)





# map for listing all dog spots
def map(request):
    latlng = geocoder.ip('me')

    map_db = Map_Details.objects.all()
    context = {'map_db': map_db, 'lat':latlng.lat, 'lng':latlng.lng}
    return render(request, 'home/map.html', context)


def donation(request):
    context = {}
    return render(request, 'home/donation.html', context)



from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Pet, Adoption
from django.db.models import Q


from django.db.models import Q
from django.core.paginator import Paginator
from .models import Pet, Adoption
from django.shortcuts import render

def pet_listing(request):
    query = request.GET.get('q', None)
    
    # Fetch all pets (whether available or adopted) by default
    pets = Pet.objects.all()

    # Apply search filter if a query is present
    if query:
        pets = pets.filter(Q(pet_name__icontains=query) | Q(pet_breed__icontains=query))

    # Pagination: 10 pets per page
    paginator = Paginator(pets, 10)
    page_number = request.GET.get('page', 1)
    pets_page = paginator.get_page(page_number)

    # Recommendation Logic
    recommendations = None

    # Search-based recommendations (if a search query is present)
    if query:
        recommendations = Pet.objects.filter(
            Q(pet_breed__icontains=query) | Q(pet_name__icontains=query),
            pet_status='Available'
        ).exclude(id__in=pets_page.object_list.values_list('id', flat=True))[:3]

    # Collaborative Filtering (if the user has adopted pets)
    if request.user.is_authenticated:
        user_adoptions = Adoption.objects.filter(user=request.user).values_list('pet_id', flat=True)
        
        if user_adoptions:
            # Find other users who adopted similar pets
            other_user_adoptions = Adoption.objects.filter(
                pet_id__in=user_adoptions
            ).exclude(user=request.user).values_list('user_id', flat=True)

            # Recommend pets adopted by similar users
            collaborative_recommendations = Pet.objects.filter(
                adoption__user_id__in=other_user_adoptions
            ).exclude(id__in=user_adoptions).distinct().order_by('?')[:3]

            # Combine search-based and collaborative recommendations if both exist
            if recommendations is None:
                recommendations = collaborative_recommendations
            else:
                recommendations |= collaborative_recommendations  # Union of querysets
                recommendations = recommendations.distinct()[:3]
    
    # Default random recommendations if there are no search results or adoptions
    if recommendations is None:
        recommendations = Pet.objects.filter(pet_status='Available').order_by('?')[:3]

    context = {
        'pets': pets_page,  # Paginated pets for the current page
        'recommendations': recommendations,  # Recommended pets
        'query': query,  # Search query passed back for the frontend form
    }

    return render(request, 'user/dashboard.html', context)




# Adopt Pet View
@login_required
def adopt_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, pet_status='Available')

    if request.method == 'POST':
        # Mark the pet as adopted
        pet.pet_status = 'Adopted'
        pet.date_adopted = timezone.now()
        pet.save()

        # Create an adoption record
        Adoption.objects.create(user=request.user, pet=pet, adoption_confirmed=True)

        return redirect('home.pet_listing')

    context = {
        'pet': pet
    }

    return render(request, 'user/adopt_pet.html', context)


# View to show the user's adoptions
@login_required
def my_adoptions(request):
    # Fetch the pets adopted by the current logged-in user
    adoptions = Adoption.objects.filter(user=request.user)

    context = {
        'adoptions': adoptions
    }

    return render(request, 'user/adopt_list.html', context)


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Pet, Adoption
from django.db.models import Q

from django.db.models import Q
from django.db.models.functions import Replace

def dashboard(request):
    query = request.GET.get('q', None)

    # Fetch all pets, whether available or adopted
    pets = Pet.objects.all()

    # Normalize search query by stripping spaces and converting to lowercase
    if query:
        query_normalized = query.strip().lower()

        # Normalize pet_breed by stripping spaces or special characters
        pets = pets.annotate(normalized_breed=Replace('pet_breed', ' ', '')).filter(
            Q(pet_name__icontains=query_normalized) |
            Q(normalized_breed__icontains=query_normalized)
        )

    # Pagination: 10 pets per page
    paginator = Paginator(pets, 10)
    page_number = request.GET.get('page', 1)  # Default to page 1
    pets_page = paginator.get_page(page_number)

    context = {
        'pets': pets_page,
        'query': query,
    }

    return render(request, 'user/dashboard.html', context)

