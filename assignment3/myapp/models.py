from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import *

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=False, default="Development")

    def __str__(self):
      return self.name

class Course(models.Model):
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(50), MaxValueValidator(500)])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        #return f"{self.name}'s costs {self.price} and it {'is' if {self.for_everyone} else 'not'} for everyone"
        return self.name

   
    def discount(self):
        discount_to_apply = self.price * Decimal(0.1)  
        self.price  = self.price - discount_to_apply
        self.save() 
        #return self.price
             




class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgery'),('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profile_pictures/', default='profile_pictures/default_profile_picture.jpeg')

    def __str__(self):
        return self.first_name



class Order(models.Model):
    ORDER_CHOICE = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=ORDER_CHOICE, default="1")
    order_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.course.name} by {self.student.first_name} {self.student.last_name}"

    def total_cost(self):
        all_price = [price for price in self.course.price]
        return sum(all_price)

    def get_order_status_verbose(self):
        return dict(self.ORDER_CHOICE)[self.order_status]