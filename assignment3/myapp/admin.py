from django.contrib import admin
from myapp.models import Order

from .models import Topic, Course, Student, Order
# Register your models here.

class CourseInline(admin.TabularInline):
    model = Course


@admin.register(Topic) 
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name','category')


    inlines = [CourseInline]



@admin.action(description="Apply 10 percent discount on the price")    
def apply_discount(modeladmin, request, queryset):
    for query in queryset:
        query.discount()

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','price')
    actions = [apply_discount]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'levels', 'Registered_Courses')

    def levels(self, obj): 
        levels = ""   
        orders = Order.objects.filter(student=obj)
        for order in orders:
            levels+=f'{order.levels}, ' 

        return levels

    def Registered_Courses(self, obj): 
        registered_courses = ""  
        orders = Order.objects.filter(student=obj)
        for order in orders:
            registered_courses+=f'{order.course.name}, ' 

        return registered_courses 


   

admin.site.register(Order)
# Register your models here.
