from django.contrib.auth.models import User
from django.db import models

country_choices = (
    ('China','China'),
    ('India','India'),
    ('United States','United States'),
    ('Indonesia','Indonesia'),
    ('Pakistan','Pakistan'),
    ('Brazil','Brazil'),
    ('Nigeria','Nigeria'),
    ('Bangladesh','Bangladesh'),
    ('Russia','Russia'),
    ('Mexico','Mexico'),
    ('Japan','Japan'),
    ('Germany','Germany'),
)

state_choices =(
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh ','Arunachal Pradesh '),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
    ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
    ('Chandigarh','Chandigarh'),
    ('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
)



city_choices = (
    ('Mumbai','Mumbai'),
    ('Pune','Pune'),
    ('Nagpur','Nagpur'),
    ('Thane','Thane'),
    ('Nashik','Nashik'),
    ('Kalyan-Dombivli','Kalyan-Dombivli'),
    ('Aurangabad','Aurangabad'),
    ('Solapur','Solapur'),
    ('Latur','Latur'),
    ('Amravati','Amravati'),
    ('Kolhapur','Kolhapur'),
    ('Akola','Akola'),
    ('Jalgaon','Jalgaon'),
    ('Dhule','Dhule'),
    ('Ahmednagar','Ahmednagar'),
    ('Chandrapur','Chandrapur'),
    ('Parbhani','Parbhani'),
    ('Solapur','Solapur'),
    ('Wardha','Wardha'),
    ('Nandurbar','Nandurbar'),

)


GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female')
)

CATEGARY_CHOICES= (
    ('Mobile','Mobile'),
    ('Laptop','Laptop'),
    ('Charger','Charger'),
    ('Headphone','Headphone'),
    ('Print','Print'),
    ('Top Wear','Top Wear'),
    ('Bottom Wear','Bottom Wear'),
    ('Electronic','Electronic'),
    ('HK','Home & Kitchen'),
    ('Books','Books'),
    ('Shoes','Shoes'),
    ('Garden','Garde '),
    ('Handmade','Handmade'),
    ('Kitchen','Kitchen'),
    ('Kindle','Kindle'),
    ('Travel Gear','Travel Gear'),
    ('Movies','Movies'),
    ('Musical Instruments','Musical Instruments'),
    ('Sports','Sports'),
    ('Toys','Toys'),
)

class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=200)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    product_category = models.CharField(max_length=70 ,choices=CATEGARY_CHOICES)
    country = models.CharField(max_length=200, choices=country_choices)
    state = models.CharField(max_length=200, choices=state_choices)
    city = models.CharField(max_length=200, choices=city_choices)
    bank_name = models.CharField(max_length=200)
    account_no = models.CharField(max_length=200)
    gst_no = models.PositiveIntegerField()
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)