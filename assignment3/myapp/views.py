from django.http  import HttpResponse
from .models import Topic, Course, Student, Order
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
