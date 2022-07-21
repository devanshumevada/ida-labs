from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Topic, Course, Student, Order
from .forms import OrderForm, InterestForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.
# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 'Your last login was more than one hour ago'
    return render(request, 'myapp/index.html', {'top_list': top_list, 'last_login': last_login})


def about(request):
    if 'about_visits' in request.session:
        request.session['about_visits'] += 1
    else:
        request.session['about_visits'] = 1
        request.session.set_expiry(300)

    return render(request, 'myapp/about.html', {'about_visits': request.session['about_visits']})


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



def user_login(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            print("Cookie Working")
        else:
            print("Not Working Cookie")
        username = request.POST['username']
        password = request.POST['password']
        #print(f'Username: {username})
        
        user = authenticate(username=username, password=password) 
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        
        else:return HttpResponse('Invalid login details.') 
    else:
        request.session.set_test_cookie()
        return render(request, 'myapp/login.html')
    
    
        
        
@login_required
def user_logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return HttpResponseRedirect(reverse('myapp:index'))

@login_required(login_url='/myapp/login/') 
def myaccount(request):
    username = request.user.username 
    try:   
        user = Student.objects.filter(username=username)
    except: 
        user = None
    is_student = False
    orders = None 
    if user:
        is_student = True
        orders = Order.objects.filter(student=user[0])
        topics = Student.objects.get(username=username).interested_in.values()
        #print(orders)    
        #print(topics)
        return render(request, 'myapp/myaccount.html', {'is_student': is_student, 'orders': orders, 'topics': topics})
    
    return render(request, 'myapp/myaccount.html', {'is_student':is_student})

