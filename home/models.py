from django.db import models
from django.utils import timezone
from django.conf import settings

class Pet(models.Model):
    # Pet model as defined earlier
    pet_name = models.CharField(max_length=100, default="Unknown Pet")
    pet_breed = models.CharField(max_length=100, default="Unknown Breed")
    pet_age = models.IntegerField(default=0)  
    pet_status = models.CharField(
        max_length=50, 
        choices=[('Available', 'Available'), ('Adopted', 'Adopted')], 
        default='Available'
    )
    pet_gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female')],
        default='Male'
    )
    pet_size = models.CharField(
        max_length=20, 
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')],
        default='Medium'
    )
    pet_color = models.CharField(max_length=50, default='Unknown')
    health_status = models.CharField(max_length=100, default='Healthy')
    vaccinated = models.BooleanField(default=False)
    spayed_neutered = models.BooleanField(default=False)
    special_needs = models.CharField(max_length=255, blank=True, null=True)
    location_city = models.CharField(max_length=100, default='Unknown Location')
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_adopted = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='pet_images/', null=True, blank=True)

    def __str__(self):
        return self.pet_name


class Adoption(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adoption_date = models.DateTimeField(auto_now_add=True)
    adoption_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} adopted {self.pet.pet_name}'


from django.db import models
from django.utils import timezone

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100, choices=[('Contact Us', 'Contact Us'), ('Feedback', 'Feedback')], default='Contact Us')
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
