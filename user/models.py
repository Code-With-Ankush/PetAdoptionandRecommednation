from django.db import models
from accounts.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Model for storing map-related details
class Map_Details(models.Model):

    ZONE_COLORS = [
        ('red', 'Red'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
    ]
    
    RADIUS_COLORS = [
        ('#FF0000', 'Red'),
        ('#FFD326', 'Yellow'),
        ('#2AAD27', 'Green'),
    ]

    KM_DISTANCE = [
        ('250', '500 Meters'),
        ('500', '1 Km'),
        ('1000', '2 Km'),
        ('1500', '3 Km'),
        ('2000', '4 Km'),
        ('2500', '5 Km'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True)
    place_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    no_of_dogs = models.IntegerField(null=True, blank=True)
    behaviour = models.CharField(max_length=255, null=True, blank=True)
    zone = models.CharField(max_length=50, choices=ZONE_COLORS)
    radius_color = models.CharField(max_length=50, choices=RADIUS_COLORS)
    radius_color_hexcode = models.CharField(max_length=50, choices=RADIUS_COLORS)
    km_distance = models.IntegerField(choices=KM_DISTANCE)

    def __str__(self):
        return f"{self.place_name} - {self.user.username}"


# Model for storing pictures of dogs and pet details related to map points
class Dog_Pics(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    ]

    PET_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Adopted', 'Adopted'),
    ]

    PET_GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    PET_SIZE_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]

    # Foreign key relation to the Map_Details model, with a related name
    map_id = models.ForeignKey('Map_Details', on_delete=models.CASCADE, related_name='dog_pics', null=True, default=None)
    
    # Image field allowing null and blank values with default set to None
    image = models.ImageField(upload_to='dog_images/', null=True, blank=True, default=None)
    
    # Status field with predefined choices and default value 'Pending'
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending', null=True)

    # Pet details fields
    pet_name = models.CharField(max_length=100, default="Unknown Pet")
    pet_breed = models.CharField(max_length=100, default="Unknown Breed")
    pet_age = models.IntegerField(default=0)  
    pet_status = models.CharField(max_length=50, choices=PET_STATUS_CHOICES, default='Available')
    pet_gender = models.CharField(max_length=10, choices=PET_GENDER_CHOICES, default='Male')
    pet_size = models.CharField(max_length=20, choices=PET_SIZE_CHOICES, default='Medium')
    pet_color = models.CharField(max_length=50, default='Unknown')
    health_status = models.CharField(max_length=100, default='Healthy')
    vaccinated = models.BooleanField(default=False)
    spayed_neutered = models.BooleanField(default=False)
    
    # DateTime field for upload time, allowing null values
    uploaded_at = models.DateTimeField(null=True, default=None)

    def save(self, *args, **kwargs):
        # Optional image compression logic, compresses image before saving
        if self.image:
            img = Image.open(self.image)
            img = img.convert("RGB")
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG', quality=80)
            self.image = ContentFile(img_bytes.getvalue(), self.image.name)
        super().save(*args, **kwargs)

        # Logic to notify the user on approval status
        if self.status == 'Approved':
            # Notify the user, possibly via email or another method, that their pet adoption request is approved
            # You can integrate email functionality here if required.
            pass

    def __str__(self):
        return f"Dog picture for map point {self.map_id}"

    class Meta:
        verbose_name = 'Dog Picture'
        verbose_name_plural = 'Dog Pictures'
