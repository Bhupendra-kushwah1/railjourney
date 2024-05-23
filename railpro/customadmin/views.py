
from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from loginapp.models import Train


# customadmin login
def adminlogin(request):
    try:
        if request.user.is_authenticated:
            return redirect('/')
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            User_obj = User.objects.filter(username = username)
            if not User_obj.exists():
                messages.info(request, 'account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username = username, password=password)

            if user_obj and user_obj.is_superuser:
                login(request , user_obj)
                return redirect('/addtrain/')
            messages.info(request , 'Invalid Password')
            return redirect('/')
        return render(request, 'login.html')
    except Exception as e:
        print(e)


#custom admin logout
def adminlogout(request):
    try:
        logout(request)
        return redirect('/')
    except Exception as e:
        print(e)        


#for train addition by admin
def addtrain(request):
    if request.method == "POST":
          train_name =request.POST.get('train_name')
          train_no = request.POST.get('train_no')
          destination = request.POST.get('destination')
          origin_station=request.POST.get('origin_station')
          sleeper_seats=request.POST.get('sleeper_seats')
          ac3_seats=request.POST.get('ac3_seats')
          ac2_seats=request.POST.get('ac2_seats')
          ac1_seats=request.POST.get('ac1_seats')
          sleeper_fare=request.POST.get('sleeper_fare')
          ac3_fare=request.POST.get('ac3_fare')
          ac2_fare=request.POST.get('ac2_fare')
          ac1_fare=request.POST.get('ac1_fare')
          Addtrain = Train.objects.create(train_name=train_name, train_no=train_no,destination=destination,origin_station=origin_station,
                             sleeper_seats=sleeper_seats,ac3_seats=ac3_seats,ac2_seats=ac2_seats,ac1_seats=ac1_seats,sleeper_fare=sleeper_fare,
                              ac3_fare=ac3_fare,ac2_fare=ac2_fare, ac1_fare=ac1_fare )
          Addtrain.save()
    return render(request, 'addtrain.html') 


#for train cancellation by admin
def canceltrain(request):
    message = None
    if request.method == 'POST':
        train_no = request.POST.get('train_no')
        try:
            train = Train.objects.get(train_no=train_no)
            # Delete the train
            train.delete()
            message = 'Train successfully deleted.'
        except Train.DoesNotExist:
            message = 'Train with the given number does not exist.'
    return render(request, 'cancel_train.html', {'message': message})


# for trains list by admin
def trainslist(request):
    trains = Train.objects.all()
    return render(request, 'train_list.html', {'trains': trains})

#delete train by searching pnr
def deletetrain(request, train_no):
    trains = Train.objects.get(train_no = train_no)
    trains.delete()
    message = 'Train successfully deleted.'
    return redirect('trainslist')


#for updating trains data
def update(request,train_no):
    if request.method=='GET':
        data = Train.objects.get(train_no=train_no)
        return render(request,'updatetrain.html',{'data':data})
    
    elif  request.method == 'POST':
          data = Train.objects.get(train_no=train_no)
          data.train_name =request.POST.get('train_name')
          data.train_no = request.POST.get('train_no')
          data.destination = request.POST.get('destination')
          data.origin_station=request.POST.get('origin_station')
          data.total_time =request.POST.get('total_time')
          data.arrival_time= request.POST.get('arrival_time')
          data.departure_time=request.POST.get('departure_time')
          data.sleeper_seats=request.POST.get('sleeper_seats')
          data.ac3_seats=request.POST.get('ac3_seats')
          data.ac2_seats=request.POST.get('ac2_seats')
          data.ac1_seats=request.POST.get('ac1_seats')
          data.sleeper_fare=request.POST.get('sleeper_fare')
          data.ac3_fare=request.POST.get('ac3_fare')
          data.ac2_fare=request.POST.get('ac2_fare')
          data.ac1_fare=request.POST.get('ac1_fare')
          data.save()
          return redirect('trainslist')
        

        