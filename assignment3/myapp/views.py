from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Topic, Course, Student, Order
from .forms import OrderForm, InterestForm, ProfilePictureUploadForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime


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

@login_required(login_url='/myapp/login/')
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
        next = request.POST.get('next',None)
        #print(f'Username: {username})
        
        user = authenticate(username=username, password=password) 
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(0) 
                if not next:
                    return HttpResponseRedirect(reverse('myapp:index'))
                
                return HttpResponseRedirect(next)
            else:
                return HttpResponse('Your account is disabled.')
        
        else:return HttpResponse('Invalid login details.') 
    else:
        if request.user.is_authenticated:
            return redirect('myapp:index')
        request.session.set_test_cookie()
        username_to_fill = request.GET.get('username', None) 
        print(username_to_fill)
        return render(request, 'myapp/login.html', {'username_to_fill': username_to_fill})
    
    
        
        
@login_required(login_url='/myapp/login/')
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

    if request.method == 'POST':
        profile_picture_upload_form = ProfilePictureUploadForm(request.POST, request.FILES, instance=user[0])
        password = request.POST['password']
        if profile_picture_upload_form.is_valid():
            user_object = profile_picture_upload_form.save()
            if password: 
                user_object.set_password(password)
                user_object.save()

        return redirect('myapp:myaccount')

   
    is_student = False
    orders = None 
    if user:
        is_student = True
        orders = Order.objects.filter(student=user[0])
        topics = Student.objects.get(username=username).interested_in.values()
        if len(topics) == 0:
            topics = []
        profile_picture_upload_form = ProfilePictureUploadForm(instance=user[0])
        #print(orders)    
        #print(topics)
        return render(request, 'myapp/myaccount.html', {'user':user[0],'is_student': is_student, 'orders': orders, 'topics': topics, 'form':profile_picture_upload_form})
    
    return render(request, 'myapp/myaccount.html', {'is_student':is_student})


def register_student(request):

    if request.method == 'POST':


        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']


        try:
            student = get_object_or_404(Student, username=username)
        except:     
            student = None

        if not username or not password:
            return render(request, 'myapp/register.html', {'error_message': 'Either username or password or both have not been passed'})

        if student:
            return render(request, 'myapp/register.html', {'error_message': 'User already exists with the given username'})

        
        student = Student.objects.create_user(username=username, password=password, email=email)
        student.first_name = username  
        student.save()

        return redirect(reverse('myapp:login') + f'?username={username}')



    if request.user.is_authenticated:
        return redirect('myapp:index')
    return render(request, 'myapp/register.html')


@login_required(login_url='/myapp/login/')
def myorders(request):
    try: 
        student = Student.objects.get(username=request.user.username)
    except Student.DoesNotExist:
        student = None

    if not student:   
        return render(request, 'myapp/myorders.html', {'error_message':'You are not a registered student'})

    orders = Order.objects.filter(student=student) 
    if not orders:
        print('Inside')
        return render(request, 'myapp/myorders.html', {'error_message': 'You do not have any orders'})      
    return render(request, 'myapp/myorders.html', {'orders':orders})   


@login_required(login_url='/myapp/login/')
def handle_image_upload(request):    
    if request.method == 'POST':  
        pass


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        student = Student.objects.get(email=email)

        if student: 
            random_password = Student.objects.make_random_password()   
            #print(random_password)    
            student.set_password(random_password)
            student.save()
            send_mail(
                
                subject=f'{student.first_name}: Here is your new password', 
                message=f'Your new password is: {random_password}. Please change your password from myaccount page',
                from_email = "dm.25041998@gmail.com" ,
                recipient_list=[student.email,],
                fail_silently=False
            
            )

        return  redirect('myapp:login')



        
    return render(request, 'myapp/forgot_password.html')

