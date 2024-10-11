from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

# Extending custom User model fields
class User(AbstractUser):
    ROLE_CHOICE = [
        ("admin", "admin"),
        ("user", "user")
    ]
    STATUS_CHOICE = [
        ("active", "active"),
        ("suspend", "suspend"),
        ("ban", "ban")
    ]


    STATE_CHOICES = [
        ("province_1", "Province 1"),
        ("province_2", "Province 2"),
        ("bagmati", "Bagmati"),
        ("gandaki", "Gandaki"),
        ("lumbini", "Lumbini"),
        ("karnali", "Karnali"),
        ("sudurpaschim", "Sudurpaschim"),
    ]

    DISTRICT_CHOICES = [
        # Province 1
        ("bhojpur", "Bhojpur"),
        ("dhankuta", "Dhankuta"),
        ("ilam", "Ilam"),
        ("jhapa", "Jhapa"),
        ("khotang", "Khotang"),
        ("morang", "Morang"),
        ("okhaldhunga", "Okhaldhunga"),
        ("sankhuwasabha", "Sankhuwasabha"),
        ("solukhumbu", "Solukhumbu"),
        ("sunsari", "Sunsari"),
        ("taplejung", "Taplejung"),
        ("terhathum", "Terhathum"),
        ("udayapur", "Udayapur"),
        
        # Province 2
        ("bara", "Bara"),
        ("dhanusa", "Dhanusa"),
        ("mahottari", "Mahottari"),
        ("parsa", "Parsa"),
        ("rautahat", "Rautahat"),
        ("saptari", "Saptari"),
        ("sarlahi", "Sarlahi"),
        ("siraha", "Siraha"),

        # Bagmati Province
        ("bhaktapur", "Bhaktapur"),
        ("chitwan", "Chitwan"),
        ("dhading", "Dhading"),
        ("dolakha", "Dolakha"),
        ("kathmandu", "Kathmandu"),
        ("kavrepalanchok", "Kavrepalanchok"),
        ("lalitpur", "Lalitpur"),
        ("makwanpur", "Makwanpur"),
        ("nuwakot", "Nuwakot"),
        ("rasuwa", "Rasuwa"),
        ("ramechhap", "Ramechhap"),
        ("sindhuli", "Sindhuli"),
        ("sindhupalchok", "Sindhupalchok"),

        # Gandaki Province
        ("baglung", "Baglung"),
        ("gorkha", "Gorkha"),
        ("kaski", "Kaski"),
        ("lamjung", "Lamjung"),
        ("manang", "Manang"),
        ("mustang", "Mustang"),
        ("myagdi", "Myagdi"),
        ("nawalpur", "Nawalpur"),
        ("parbat", "Parbat"),
        ("syangja", "Syangja"),
        ("tanahun", "Tanahun"),

        # Lumbini Province
        ("arghakhanchi", "Arghakhanchi"),
        ("banke", "Banke"),
        ("bardiya", "Bardiya"),
        ("dang", "Dang"),
        ("gulmi", "Gulmi"),
        ("kapilvastu", "Kapilvastu"),
        ("palpa", "Palpa"),
        ("pyuthan", "Pyuthan"),
        ("rolpa", "Rolpa"),
        ("rukum_east", "Rukum East"),
        ("rupandehi", "Rupandehi"),

        # Karnali Province
        ("dailekh", "Dailekh"),
        ("dolpa", "Dolpa"),
        ("humla", "Humla"),
        ("jaumla", "Jumla"),
        ("kalikot", "Kalikot"),
        ("mugu", "Mugu"),
        ("rukum_west", "Rukum West"),
        ("salyan", "Salyan"),
        ("surkhet", "Surkhet"),

        # Sudurpaschim Province
        ("achham", "Achham"),
        ("baitadi", "Baitadi"),
        ("bajhang", "Bajhang"),
        ("bajura", "Bajura"),
        ("dadeldhura", "Dadeldhura"),
        ("darchula", "Darchula"),
        ("doti", "Doti"),
        ("kailali", "Kailali"),
        ("kanchanpur", "Kanchanpur"),
    ]

    role=models.CharField(default='user', choices=ROLE_CHOICE, max_length=50, null=True, blank=True)
    status=models.CharField(default='active', choices=STATUS_CHOICE, max_length=50, null=True, blank=True)
    profile_pic=models.ImageField(upload_to='users/profile_pic', default="default_profile_pic.png", null=True, blank=True)
    latitude=models.CharField(max_length=255, null=True, blank=True)
    longitude=models.CharField(max_length=255, null=True, blank=True)
    state=models.CharField(max_length=255, choices=STATUS_CHOICE, null=True, blank=True)
    place=models.CharField(max_length=255, null=True, blank=True)