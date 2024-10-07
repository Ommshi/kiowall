from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    categories = Category.objects.all()  
    if request.method == "POST":
        searched = request.POST.get('searched', '')  # Safely get the value
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "Dieses Produkt existiert bei uns nicht.")
            return render(request, 'search.html', {'categories': categories})  
        else:
            return render(request, 'search.html', {'searched': searched, 'categories': categories})  
    else:
        return render(request, 'search.html', {'categories': categories})  

def update_info(request):
    categories = Category.objects.all()  
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)        
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Ihre Informationen wurden aktualisiert!")
            return redirect('update_info')
        return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form, 'categories': categories})  
    else:
        messages.success(request, "Sie müssen angemeldet sein, um auf diese Seite zugreifen zu können!")
        return redirect('home')

def update_password(request):
    categories = Category.objects.all()  
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Dein Passwort wurde erfolgreich aktualisiert!')
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form, 'categories': categories})  
    else:
        messages.error(request, 'Du musst eingeloggt sein, um dein Passwort zu aktualisieren.')
        return redirect('home')

def update_user(request):
    categories = Category.objects.all()  
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "Profil wurde erfolgreich aktualisiert.")
            return redirect('home')
        return render(request, "update_user.html", {'user_form': user_form, 'categories': categories})  
    else:
        messages.success(request, "Du musst angemeldet sein, um auf diese Seite zuzugreifen.")
        return redirect('home')

def category_summary(request):
    categories = Category.objects.all()  
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

def category(request, foo):
    categories = Category.objects.all()  
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category, 'categories': categories})  
    except:
        messages.success(request, ("Diese Kategorie existiert nicht."))
        return redirect('home')

def product(request, pk):
    categories = Category.objects.all()  
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product, 'categories': categories})  

def home(request):
    categories = Category.objects.all()  
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})  

def about(request):
    categories = Category.objects.all()  
    products = Product.objects.all()
    return render(request, 'about.html', {'categories': categories})  

def login_user(request):
    categories = Category.objects.all()  
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("Du bist eingeloggt"))
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html', {'categories': categories})  

def logout_user(request):
    categories = Category.objects.all()  
    logout(request)
    messages.success(request, ("Bis zum nächsten Mal"))
    return redirect('home')

def register_user(request):
    categories = Category.objects.all()  
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Dein Konto wurde registriert"))
            return redirect('home')
        else:
            messages.success(request, ("Upps, bei der Registrierung ist ein Problem aufgetreten. Bitte versuche es erneut."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form, 'categories': categories})  
