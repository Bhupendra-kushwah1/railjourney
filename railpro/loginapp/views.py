
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from .middlewares import auth 
from .models import Train
from .models import Ticketghar
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User

#the base page where all starts
def home_view(request):
    return render(request, 'home.html') 


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send a confirmation email to the user with username and password
            subject = 'Welcome to Our Site'
            message = f'Hi {user.username},\n\nThank you for registering with us. Your account has been created successfully.\n\nUsername: {user.username}\nPassword: {form.cleaned_data["password1"]}'
            from_email = 'bhupendraslaptop@gmail.com'  # Replace with your email address
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            login(request, user)
            return redirect('home')
    else:
        initial_data = {'username': '', 'email': '', 'password1': '', 'password2': '', 'first_name': '', 'last_name': ''}
        form = CustomUserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html', {'form': form})


#for logging in by the users
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial = initial_data)  
    return render(request, 'auth/login.html', {'form':form}) 
   
#for logging out user
def logout_view(request):
    logout(request)
    return redirect('login')

# for viewing dashboard of user
@auth
def dashboard_view(request):
    return render(request, 'dashboard.html')

#ticket booking page
@auth
def bookticket_view(request):
    return render(request, 'bookticket.html') 

def saveticket(request):
    if request.method == "POST":
        # Retrieve the current user
        user = request.user
        
        # Extract data from the request
        train_name = request.POST.get('train_name')
        train_no = request.POST.get('train_no')
        destination = request.POST.get('destination')
        origin_station = request.POST.get('origin_station')
        train_class = request.POST.get('train_class')
        copassengers = request.POST.get('copassengers')
        total_fare = request.POST.get('total_fare')
        head = request.POST.get('head')
        passage = request.POST.get('passage')
        gender = request.POST.get('gender')
        train_date = request.POST.get('train_date')
        
        # Create and save the Ticketghar object with the user as foreign key
        Addticket = Ticketghar.objects.create(
            user=user,
            train_name=train_name,
            train_no=train_no,
            destination=destination,
            origin_station=origin_station,
            train_class=train_class,
            copassengers=copassengers,
            total_fare=total_fare,
            head=head,
            passage=passage,
            gender=gender,
            train_date=train_date
        )
        # Optionally, handle errors or provide feedback to the user
        
        return redirect('ticketgenerate')  # Redirect to a success page or detail view
        
    return render(request, 'booktrain.html')



@auth
def print_user_tickets(request):
    # Get the logged-in user
    logged_in_user = request.user
    
    # Query all tickets associated with the logged-in user
    user_tickets = Ticketghar.objects.filter(user=logged_in_user)
    
    # Prepare the HTML content of the email
    html_content = render_to_string('ticketgenerate.html', {'user_tickets': user_tickets})
    
    # Create the EmailMultiAlternatives object
    subject = 'Your Tickets'
    text_content = strip_tags(html_content)  # Convert HTML to plain text
    email = EmailMultiAlternatives(subject, text_content, to=[logged_in_user.email])
    
    # Attach the HTML content
    email.attach_alternative(html_content, "text/html")
    
    # Send the email
    email.send()
    
    # Assuming you want to return something after sending the email
    return render(request, 'ticketgenerate.html', {'user_tickets': user_tickets})



@auth
def cancelticket_view(request):
    if request.method == 'GET':
        # Get the pnr from the query parameters
        pnr = request.GET.get('pnr')

        # Check if pnr is provided
        if not pnr:
            messages.error(request, '')
            return render(request, 'cancelticket.html')

        # Get the ticket instance
        try:
            ticket = Ticketghar.objects.get(pnr_no=pnr)
        except Ticketghar.DoesNotExist:
            messages.error(request, 'Invalid PNR, Please Enter a valid PNR')
            return render(request, 'cancelticket.html')

        # Check if the ticket belongs to the logged-in user
        if ticket.user != request.user:
            messages.error(request, 'You are not authorized to delete this ticket')
            return render(request, 'cancelticket.html')

        # Compose the email message
        subject = 'Ticket Cancellation Confirmation'
        message = f"Your ticket with PNR number {pnr} has been cancelled successfully."

        # Send email to the logged-in user
        from_email = 'bhupendraslaptop@gmail.com'  # Change to your email address
        to_email = [request.user.email]
        send_mail(subject, message, from_email, to_email)

        # Delete the ticket
        ticket.delete()

        # Set success message
        messages.success(request, 'Ticket cancelled successfully')

    # Redirect or render the same page
    return render(request, 'cancelticket.html')



def search_pnr(request):
    if request.method == 'POST':
        pnr = request.POST.get('pnr_number')
        try:
            ticket = Ticketghar.objects.get(pnr_no=pnr, user=request.user)
            return render(request, 'pnr_details.html', {'ticket': ticket})
        except Ticketghar.DoesNotExist:
            return render(request, 'search_pnr.html', {'error_message': 'Invalid PNR'})

    return render(request, 'search_pnr.html')


@auth
def search_trains(request):
    if request.method == 'POST':
        origin_station = request.POST.get('origin_station')
        destination = request.POST.get('destination')
        matching_trains = Train.objects.filter(origin_station=origin_station, destination=destination)
        return render(request, 'bookticket.html', {'trains': matching_trains})
    # return render(request, 'search_form.html')


 #for getting form filled when user clicks on book now

@auth
def booknow(request,train_no):
    if request.method=='GET':
        data = Train.objects.get(train_no=train_no)
        return render(request,'booktrain.html',{'data':data})



def about_us_view(request):
    return render(request, 'aboutus.html')


def contact_us_view(request):
    return render(request, 'contact_us.html')

def contact_us_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Compose and send the email
        subject = 'New Contact Form Submission'
        email_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        sender_email = email  # Use the email entered by the user as the sender's email address
        receiver_email = 'bhupendraslaptop@gmail.com'

        try:
            send_mail(subject, email_body, sender_email, [receiver_email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        # Redirect to a thank you page after sending the email
        return redirect('home') 

    return render(request, 'contact_us.html')
