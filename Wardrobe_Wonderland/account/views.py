from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email
from .forms import UserCreateForm, UserLoginForm, UserUpdateForm
from shop.models import Category
from django.contrib.auth.views import PasswordResetConfirmView
from .forms import CustomSetPasswordForm

User = get_user_model()


def register_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            # Create new user
            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )

            user.is_active = False

            send_email(user)

            return redirect('account:email_verification_sent')

    else:
        form = UserCreateForm()

    categories = Category.objects.filter(status=True)

    return render(request, 'registration.html', {'form': form, 'categories': categories})


def login_user(request):
    form = UserLoginForm()

    if request.user.is_authenticated:
        return redirect('category')

    if request.method == 'POST':
        form = UserLoginForm(request.POST, request.FILES)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('account:login')
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('category')


@login_required(login_url='account:login')
def dashboard_user(request):
    categories = Category.objects.filter(status=True)
    context = {
        'categories': categories
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='account:login')
def profile_user(request):
    categories = Category.objects.filter(status=True)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('account:dashboard')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'dashboard/profile_management.html', context)


@login_required(login_url='account:login')
def delete_user(request):
    categories = Category.objects.filter(status=True)
    context = {
        'categories': categories
    }

    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('category')
    return render(request, 'dashboard/account_delete.html', context)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm