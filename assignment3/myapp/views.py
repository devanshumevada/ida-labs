from django.shortcuts import get_object_or_404, render, redirect
from .models import Topic, Course, Student, Order
from .forms import OrderForm, InterestForm

from django.shortcuts import get_object_or_404, render
# Create your views here.
# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


def about(request):
   return render(request, 'myapp/about.html')


def detail(request, top_no):
    topic = get_object_or_404(Topic, pk=top_no)
    courses = Course.objects.filter(topic=topic)
    return render(request, 'myapp/detail.html', {'topic': topic, 'courses': courses})  


def courses(request): 
    courlist = Course.objects.all().order_by('id') 
    return render(request, 'myapp/courses.html', {'courlist': courlist}) 


def place_order(request):
    msg = ''
    all_courses = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.course.price > 150:
                order.course.discount()
            if order.levels <= order.course.stages:
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/place_order.html', {'form': form, 'msg': msg, 'courlist': all_courses})

def course_detail(request, cour_id):
    msg = ''
    course = get_object_or_404(Course, pk=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == '1':
                course.interested = course.interested + 1
                course.save()
            return redirect('myapp:index')
        else:
            msg = 'Something went wrong'
    else:
        form = InterestForm()
    return render(request, 'myapp/course_detail.html', {'msg': msg, 'course_info': course, 'form': form})
