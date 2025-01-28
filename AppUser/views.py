from django.shortcuts import render, redirect
from AppUser.models import Customer, Cart
from AppAdmin.models import Category, Product
import re
from django.contrib import messages
from django.contrib.auth.models import User
import os

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        categoryObj = Category.objects.all()
        cartItemCount = Cart.objects.filter(user_id=userId).count()
        return render(request, 'User/Home.html', {'customer': customerObj, 'category': categoryObj, 'count': cartItemCount})
    return redirect('login')


def viewProfile(request):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        categoryObj = Category.objects.all()
        cartItemCount = Cart.objects.filter(user_id=userId).count()
        return render(request, 'User/ViewProfile.html', {'customer': customerObj, 'category': categoryObj, 'count': cartItemCount})
    return redirect('login')


def editProfile(request, id):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        categoryObj = Category.objects.all()
        userObj = User.objects.get(id=id)
        cartItemCount = Cart.objects.filter(user_id=userId).count()
        if request.method == 'POST':
            mobilePattern = re.compile(r'^[0-9]{0,10}$')
            emailPattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            email = request.POST['email']
            mobile = request.POST['mobile']
            address = request.POST['address']
            username = request.POST['username']
            if not emailPattern.match(email):
                messages.warning(request, 'Invalid email format.')
                return redirect('editProfile', id=id)
            if len(mobile) != 10 or not mobilePattern.match(mobile):
                messages.warning(request, 'Mobile number must be 10 digits.')
                return redirect('editProfile', id=id)
            if User.objects.filter(email=email).exclude(id=id).exists():
                messages.warning(request, 'Email already in use!')
                return redirect('editProfile', id=id)
            if Customer.objects.filter(mobile=mobile).exclude(user_id=id).exists():
                messages.warning(request, 'Mobile number already registered.')
                return redirect('editProfile', id=id)
            if User.objects.filter(username=username).exclude(id=id).exists():
                messages.warning(request, 'Username already taken!')
                return redirect('editProfile', id=id)
            userObj.first_name = firstName
            userObj.last_name = lastName
            if len(request.FILES)!=0:
                if len(customerObj.photo)>0:
                    os.remove(customerObj.photo.path)
                customerObj.photo = request.FILES['photo']
            userObj.email = email
            customerObj.mobile = mobile
            customerObj.address = address
            userObj.username = username
            userObj.save()
            customerObj.save()
            messages.success(request, 'Update successful.')
            return redirect('viewProfile')
        return render(request, 'User/EditProfile.html', {'customer': customerObj, 'category': categoryObj, 'count': cartItemCount})
    return redirect('login')


def viewProducts(request,id):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        categoryObj = Category.objects.all()
        productObj = Product.objects.filter(category_id=id)
        categoryObj2 = Category.objects.get(id=id)
        cartItemCount = Cart.objects.filter(user_id=userId).count()
        return render(request, 'User/ViewProducts.html', {'customer': customerObj, 'category': categoryObj, 'product': productObj, 'category2': categoryObj2, 'count': cartItemCount})
    return redirect('login')


def addToCart(request, id):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        productObj = Product.objects.get(id=id)
        userObj = User.objects.get(id=userId)
        cartItem, created = Cart.objects.get_or_create(user_id=userObj, product_id=productObj)
        if not created:
            cartItem.quantity += 1
            cartItem.save()
        messages.success(request, 'Product added to cart.')
        return redirect('viewCart')
    return redirect('login')


def viewCart(request):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        categoryObj = Category.objects.all()
        cartObj = Cart.objects.filter(user_id=userId)
        cartItemCount = Cart.objects.filter(user_id=userId).count()
        total = sum(item.totalPrice() for item in cartObj)
        return render(request, 'User/ViewCart.html', {'customer': customerObj, 'category': categoryObj, 'count': cartItemCount, 'total': total, 'cart': cartObj})
    return redirect('login')


def increaseCartQuantity(request, id):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        cartObj = Cart.objects.get(product_id=id, user_id=userId)
        cartObj.quantity += 1
        cartObj.save()
        return redirect('viewCart')
    return redirect('login')


def decreaseCartQuantity(request, id):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        cartObj = Cart.objects.get(product_id=id, user_id=userId)
        if cartObj.quantity == 1:
            cartObj.delete()
            messages.success(request, 'Product deleted from cart.')
        else:
            cartObj.quantity -= 1
            cartObj.save()
        return redirect('viewCart')
    return redirect('login')


def deleteCart(request, id):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        cartObj = Cart.objects.get(product_id=id, user_id=userId)
        cartObj.delete()
        messages.success(request, 'Product deleted from cart.')
        return redirect('viewCart')
    return redirect('login')


def checkout(request):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        categoryObj = Category.objects.all()
        cartItemCount = Cart.objects.filter(user_id=userId).count()
        return render(request, 'User/Checkout.html', {'customer': customerObj, 'category': categoryObj, 'count': cartItemCount})
    return redirect('login')


def clearCart(request):
    if request.user.is_authenticated:
        userId = request.user.id
        try:
            customerObj = Customer.objects.get(user_id=userId)
        except Exception:
            return redirect('login')
        cartObj = Cart.objects.filter(user_id=userId)
        cartObj.delete()
        messages.success(request, 'Your order is placed.')
        return redirect('viewCart')
    return redirect('login')