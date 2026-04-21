from django.shortcuts import render, redirect
from .forms import UserSignupForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from pathlib import Path
from django.template.loader import render_to_string
from django.contrib import messages

# import your models
from parking.models import Vehicle, ServiceDetail, Transportation
from django.contrib.auth import get_user_model

User = get_user_model()


# ---------------- HOME ----------------
def home(request):
    return render(request, "core/home.html")


# ---------------- SIGNUP ----------------
def userSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            # ✅ Get data
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')

            # 🔥 OPTIONAL: restrict multiple admin
            if user.role == 'admin':
                from .models import User
                if User.objects.filter(role='admin').exclude(id=user.id).exists():
                    user.delete()
                    messages.error(request, "Only one admin is allowed.")
                    return redirect('signup')

            # ✅ HTML Email
            html_content = render_to_string(
                "welcome_email.html",
                {"user_name": username}   # ✅ FIXED
            )

            email_message = EmailMultiAlternatives(
                subject="Welcome to Vehicle Vault 🚗",
                body=f"Hello {username}, Thank you for registering.",
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )

            email_message.attach_alternative(html_content, "text/html")

            # ✅ Attach file (optional)
            file_path = Path(settings.BASE_DIR) / "image.png"
            if file_path.exists():
                email_message.attach_file(file_path)

            email_message.send(fail_silently=False)

            messages.success(request, "Account created successfully!")

            return redirect('login')

        else:
            return render(request, 'core/signup.html', {'form': form})

    else:
        form = UserSignupForm()
        return render(request, 'core/signup.html', {'form': form})
# ---------------- LOGIN ----------------
def userLoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')   # ✅ use username
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)  # ✅ correct

            if user is not None:
                login(request, user)

                # 🔥 ROLE BASED REDIRECT (optional but useful)
                
                return redirect("dashboard")

            else:
                # ❌ invalid login
                return render(request, 'core/login.html', {
                    'form': form,
                    'error': 'Invalid username or password'
                })

        else:
            return render(request, 'core/login.html', {'form': form})

    else:
        form = UserLoginForm()
        return render(request, 'core/login.html', {'form': form})

# ---------------- LOGOUT ----------------
def userLogoutView(request):
    logout(request)
    return redirect('home')


# # ---------------- DASHBOARD ----------------
# @login_required(login_url="login")
# def dashboard(request):

#     role = request.user.role

#     context = {
#         "role": role,
#         "user": request.user
#     }

#     # -------- ADMIN --------
#     if role == "admin":
#         context.update({
#             "total_users": User.objects.count(),
#             "total_vehicles": Vehicle.objects.count(),
#             "total_services": ServiceDetail.objects.count(),
#             "total_transport": Transport.objects.count(),
#         })

#     # -------- USER --------
#     elif role == "user":
#         context.update({
#             "vehicles": Vehicle.objects.filter(userId=request.user),
#             "services": ServiceDetail.objects.filter(vehicleId__userId=request.user),
#             "transports": Transportation.objects.filter(userId=request.user),
#         })

#     # -------- STAFF --------
#     elif role == "staff":
#         context.update({
#             "assigned_services": ServiceDetail.objects.filter(staffId=request.user)
#         })

#     return render(request, "dashboard/dashboard.html", context)