from django.shortcuts import render
from django.shortcuts import redirect
from userauthentication.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauthentication.models import User


# Create your views here.
def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
           new_user = form.save()
           username = form.cleaned_data.get("username")
           messages.success(request, f"H {username}, Your account was created successfully.")
           new_user = authenticate(username=form.cleaned_data['email'],
                                    password = form.cleaned_data['password1']                        
           )
           login(request, new_user) 
           return redirect("core:index")
    else:
        form = UserRegisterForm()
    
    contex = {
        'form': form,
    }
    
    return render(request, "userauthentication/sign-up.html",contex)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey, You Are Already Logged In.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login Successfull !")
                return redirect("core:index")
            else:
                messages.warning(request, "User Does Not Exist, Create an Account.")

        except:
            messages.warning(request, f"User With {email} Does Not Exist")

    return render(request, "userauthentication/sign-in.html") 


def logout_view(request):
    logout(request)
    messages.success(request, "User Logged Out.")
    return redirect("userauthentication:sign-in")