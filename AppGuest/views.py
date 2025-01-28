from django.shortcuts import render, redirect
import re
from django.contrib import messages
from django.contrib.auth.models import User
from AppUser.models import Customer
from django.contrib.auth.models import auth

# Create your views here.

def home(request):
    return render(request, 'Guest/Home.html')


def signUp(request):
    if request.method == 'POST':
        mobilePattern = re.compile(r'^[0-9]{0,10}$')
        emailPattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        photo = request.FILES['photo']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if not emailPattern.match(email):
            messages.warning(request, 'Invalid email format.')
            return redirect('signUp')
        if len(mobile) != 10 or not mobilePattern.match(mobile):
            messages.warning(request, 'Mobile number must be 10 digits.')
            return redirect('signUp')
        if password == confirmPassword:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already in use!')
                return redirect('signUp')
            if Customer.objects.filter(mobile=mobile).exists():
                messages.warning(request, 'Mobile number already registered.')
                return redirect('signUp')
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already taken!')
                return redirect('signUp')
            userObj = User.objects.create_user(
                        first_name = firstName,
                        last_name = lastName,
                        email = email,
                        username = username,
                        password = password
                    )
            userObj.save()
            customerObj = Customer(mobile=mobile, photo=photo, address=address, user_id=userObj)
            customerObj.save()
            messages.success(request, 'Registration successful. You can login now!')
            return redirect('login')
        messages.warning(request, "Passwords doesn't match.")
        return redirect('signUp')
    return render(request, 'Guest/SignUp.html')


def login2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        userObj = auth.authenticate(username=username, password=password)
        if userObj is not None:
            auth.login(request, userObj)
            if userObj.is_staff:
                return redirect('adminHome')
            return redirect('userHome')
        messages.warning(request, 'Invalid username or password')
        return redirect('login')
    return render(request, 'Guest/Login.html')


def logout2(request):
    auth.logout(request)
    return redirect('guestHome')