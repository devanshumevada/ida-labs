from django.contrib import admin

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
    actions = [apply_discount]


admin.site.register(Student)
admin.site.register(Order)
# Register your models here.
