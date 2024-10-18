from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required(login_url='login/')
def landing_page(request):
    return render(request, 'landing_page.html') 

def home_page(request):
    return render(request, 'home_page.html')

@require_http_methods(["GET","POST"])
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home_page')  # redirect to the home page after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm(request)
        
        
    context = {'form': form}
    return render(request, 'login.html', context)


    