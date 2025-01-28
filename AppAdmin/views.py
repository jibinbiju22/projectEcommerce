from django.shortcuts import render, redirect
from AppAdmin.models import Category, Product
from django.contrib import messages
from django.db.models import Q
import os
from AppUser.models import Customer
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'Admin/Home.html')
    return redirect('login')


def addCategory(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            categoryName = request.POST['category']
            if Category.objects.filter(category_name=categoryName):
                messages.warning(request, 'Category already registered.')
                return redirect('addCategory')
            categoryObj = Category(category_name=categoryName)
            categoryObj.save()
            messages.success(request, 'Category added successfully.')
            return redirect('addCategory')
        return render(request, 'Admin/AddCategory.html')
    return redirect('login')


def addProduct(request):
    if request.user.is_authenticated and request.user.is_staff:
        categoryObj = Category.objects.all()
        if request.method == 'POST':
            productName = request.POST['productName']
            photo = request.FILES['photo']
            description = request.POST['description']
            price = request.POST['price']
            temp = request.POST['categoryId']
            categoryId = Category.objects.get(id=temp)
            if Product.objects.filter((Q(product_name=productName) & Q(category_id=categoryId))).exists():
                messages.warning(request, 'Product already registered.')
                return redirect('addProduct')
            productObj = Product(product_name=productName, photo=photo, description=description, price=price, category_id=categoryId)
            productObj.save()
            messages.success(request, 'Product added successfully.')
            return redirect('addProduct')
        return render(request, 'Admin/AddProduct.html', {'category': categoryObj})
    return redirect('login')


def viewProduct(request):
    if request.user.is_authenticated and request.user.is_staff:
        productObj = Product.objects.all()
        return render(request, 'Admin/ViewProduct.html', {'product': productObj})
    return redirect('login')


def deleteProduct(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        productObj = Product.objects.get(id=id)
        if productObj.photo and os.path.isfile(productObj.photo.path):
            os.remove(productObj.photo.path)
        productObj.delete()
        messages.success(request, 'Product deleted.')
        return redirect('viewProduct')
    return redirect('login')


def editProduct(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        productObj = Product.objects.get(id=id)
        categoryObj = Category.objects.all()
        if request.method == 'POST':
            productName = request.POST['productName']
            description = request.POST['description']
            price = request.POST['price']
            temp = request.POST['categoryId']
            categoryId = Category.objects.get(id=temp)
            if Product.objects.filter((Q(product_name=productName) & Q(category_id=categoryId))).exclude(id=id).exists():
                messages.warning(request, 'Product already registered.')
                return redirect('editProduct', id=id)
            productObj.product_name = productName
            if len(request.FILES)!=0:
                if len(productObj.photo)>0:
                    os.remove(productObj.photo.path)
                productObj.photo = request.FILES['productPhoto']
            productObj.description = description
            productObj.price = price
            productObj.category_id = categoryId
            productObj.save()
            messages.success(request, 'Update successful.')
            return redirect('viewProduct')
        return render(request, 'Admin/EditProduct.html', {'product': productObj, 'category': categoryObj})
    return redirect('login')


def viewUser(request):
    if request.user.is_authenticated and request.user.is_staff:
        customerObj = Customer.objects.all()
        return render(request, 'Admin/ViewUser.html', {'customer': customerObj})
    return redirect('login')


def deleteUser(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        customerObj = Customer.objects.get(user_id=id)
        userObj = User.objects.get(id=id)
        if customerObj.photo and os.path.isfile(customerObj.photo.path):
            os.remove(customerObj.photo.path)
        customerObj.delete()
        userObj.delete()
        messages.success(request, 'Customer data deleted.')
        return redirect('viewUser')
    return redirect('login')