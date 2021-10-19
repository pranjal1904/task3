from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from account.models import *
from .Google import *
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            print(form.errors.as_json())
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('customer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def admin(request):
    return render(request,'admin.html')


def customer(request):
    blogs=blog.objects.all()
    data={'blogs':blogs}
    return render(request,'customer.html',data)


def employee(request):
    blogs=blog.objects.all().filter(docid=request.user.id)
    data={'blogs':blogs}
    return render(request,'employee.html',data)

def blogs(request):
    return render(request,'blog.html')


@csrf_exempt
def saveblog(request):
    if(request.method=='POST'):
        formData=request.POST
        b=blog()
        b.title=formData['title']

        if len(request.FILES) != 0:
            b.image=request.FILES['blogimage']
            
        b.category=formData['category']
        b.summary=formData['summary']
        b.content=formData['content']
        b.docid=formData['docid']
        b.save()

    return redirect(employee)


def bookappointment(request):
    doctors=User.objects.all()
    data={'doctors':doctors}
    return render(request,'bookappointment.html',data)


def confirmappointment(request,pk):
    doctor=User.objects.get(id=pk)
    data = {'doctor':doctor}
    return render(request,'confirmappointment.html',data)


def convert(stra):
    hr=int(stra[0]+stra[1])
    mm=int(stra[3]+stra[4])
    if(mm+45 >= 60):
        mm=mm+45-60
        hr+=1
        if(hr>24):
            hr=hr-24
    else:
        mm+=45
    
    a=str(hr)
    b=str(mm)
    return(a+':'+b)

@csrf_exempt
def saveappointment(request):
    if(request.method=='POST'):
        formData=request.POST
        doctor=User.objects.get(id=formData['docid'])
        d={}
        d['DoctorsN']=doctor.username
        d['AppointmentD']=formData['date']
        d['AppointmentST']=formData['time']
        ob = convert(d['AppointmentST'])
        d['AppointmentET']=ob
        request_body={
            'summary':'You have a Appointment'
        }
        response = service.calendars().insert(body=request_body).execute()
        return render(request,'bookingcompleted.html',d)