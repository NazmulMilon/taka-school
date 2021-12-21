from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import User


def user_login(request):
    USER_LOGIN_URL = 'user_login.html'
    ADMIN_LOGIN_URL = 'admin_login.html'
    USER_LOGIN_REDIRECT_URL = 'auction:dashboard'

    next = request.GET.get('next', None)  # url's next value

    if request.user.is_authenticated:
        if next:
            return redirect(next)
        return redirect(USER_LOGIN_REDIRECT_URL)

    # ***ADMIN LOGIN***
    if request.path == '/admin/':
        if request.method == "POST":
            # catch data from post request
            username = request.POST.get('username')
            password = request.POST.get('password')

            # validating data
            if username.strip() == "" or password == "":
                messages.warning(
                    request,
                    'You must have to provide both credentials!'
                )
                return render(request, ADMIN_LOGIN_URL)

            if not User.objects.filter(
                    username=username,
                    is_admin=True
            ).exists():
                messages.warning(
                    request,
                    'There is no admin with this username!'
                )
                return render(request, ADMIN_LOGIN_URL)
            else:
                admin_email = User.objects.get(
                    username=username, is_admin=True).email
                authenticated_admin = authenticate(
                    request,
                    email=admin_email,
                    password=password
                )
                if authenticated_admin is not None:
                    login(request, authenticated_admin)
                    return redirect(USER_LOGIN_REDIRECT_URL)
                else:
                    messages.error(request, 'Invalid Credentials!')
                    return render(request, ADMIN_LOGIN_URL)
        return render(request, ADMIN_LOGIN_URL)

    # ***USER LOGIN***
    else:
        if request.method == "POST":
            # catch data from post request
            email = request.POST.get('email')

            # validating data
            if email.strip() == "":
                messages.warning(request, 'You must have to provide an email!')
                return render(request, USER_LOGIN_URL)

            # Username validation
            elif User.objects.filter(
                    username=email.split('@')[0]
            ).exclude(username=email.split('@')[0]).exists():
                messages.warning(request, 'Please change the email prefix')
                return render(request, USER_LOGIN_URL)

            # If the inserted email is not in the db create a new user with
            # that email and extract username from that email and login.
            elif not User.objects.filter(
                    email=email
            ).exists() and not User.objects.filter(
                username=email.split('@')[0]
            ).exists():
                try:
                    user = User()
                    user.email = email
                    user.username = email.split('@')[0]
                    user.save()
                    login(request, user)
                    return redirect(USER_LOGIN_REDIRECT_URL)
                except Exception as e:
                    # print(e)
                    messages.error(request, f'Error: {e}')
                    return redirect('authentication:user-login')

            else:
                requested_user = User.objects.get(email=email)

                if requested_user:
                    login(request, requested_user)
                    return redirect(USER_LOGIN_REDIRECT_URL)
                else:
                    messages.error(request, 'Invalid!')
                    return render(request, USER_LOGIN_URL)

    return render(request, 'user_login.html')


@login_required(login_url='authentication:user-login')
def logout(request):
    """ Logs out the logged in user """
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('authentication:user-login')
