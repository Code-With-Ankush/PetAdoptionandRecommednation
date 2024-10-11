from django.urls import path
from home.views import index, map, donation, pet_listing, adopt_pet, my_adoptions
from .views import contact_view,pet_detail


urlpatterns = [
    path('', index, name='home.index'),  # Home page URL
    path('map/', map, name='home.map'),  # Map view URL
    path('donation/', donation, name='home.donation'),  # Donation view URL
    path('dashboard/', pet_listing, name='home.pet_listing'),  # Pet listing view URL
    path('adopt/<int:pet_id>/', adopt_pet, name='home.adopt_pet'),  # Adopt pet view URL
    path('my-adoptions/', my_adoptions, name='home.my_adoptions'),  # User's adoption history view URL
    path('contact/', contact_view, name='home.contact'),
    path('pet/<int:pet_id>/', pet_detail, name='pet_detail'),




  ]