from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib import messages
from .forms import (
    LoginForm, 
    UserRegistrationForm,
    UpdateUserForm, 
    UpdateProfileForm
)
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass

        if user is None or user.id == request.user.id:
            user_form = UpdateUserForm(
                instance=request.user, 
                data=request.POST
            )
            profile_form = UpdateProfileForm(
                instance=request.user.profile,
                data=request.POST,
            )

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

                messages.success(request, 'Profile was updated successfully')
        else:
            messages.error(request, 'User with given email already exists')

        return redirect('profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(
        request,
        'accounts/profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cf = user_form.cleaned_data

            email = cf['email']
            password = cf['password']
            password2 = cf['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 
                        'User with given email already exists')
                    return render(
                        request,
                        'accounts/register.html',
                        {'user_form': user_form}
                    )
            else:
                messages.error(request, 'Passwords don\'t match')
                return render(
                        request,
                        'accounts/register.html',
                        {'user_form': user_form}
                    )
            # Create a new user object
            new_user = User.objects.create_user(
                first_name=cf['first_name'],
                last_name=cf['last_name'],
                username=email,
                email=email,
                password=password
            )

            # Create the user profile
            Profile.objects.create(user=new_user)

            return render(
                request,
                'accounts/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'accounts/register.html',
        {'user_form': user_form}
    )

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cf = form.cleaned_data
            user_record = None
            try:
                user_record = User.objects.get(email=cf['email'])
            except User.DoesNotExist:
                pass

            if user_record:
                user = authenticate(
                    request,
                    username=user_record,
                    password=cf['password']
                )

                if user is not None:
                    login(request, user)
                    return redirect('listings:product_list')
            
            messages.error(request, 'Incorrect email / password')
        
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
