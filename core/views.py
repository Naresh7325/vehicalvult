from django.shortcuts import render,redirect
from .forms import UserSignupForm , UserLoginForm
from django.contrib.auth import authenticate,login , logout 
# from django.core.mail import send_mail
from django.core.mail import EmailMessage , EmailMultiAlternatives
from django.conf import settings
from pathlib import Path
from django.template.loader import render_to_string
# Create your views here.

def home(request):
    return render(request, "core/home.html")

def userSignupView(request):
    if request.method =="POST":
      form = UserSignupForm(request.POST or None)
      if form.is_valid():
        user=form.save()
        Email = form.cleaned_data['email']

        # Load HTML template
        html_content = render_to_string(
            "welcome_email.html",   # because it's inside main templates folder
            {
                "user_name": user.email
            } 
        )

        email_message = EmailMultiAlternatives(
            subject="Welcome to Vehicle Valut 🚗",
            body="Thank you for registering with Vehicle Vault.",
            from_email=settings.EMAIL_HOST_USER,
            to=[Email],
        )

        # Attach HTML
        email_message.attach_alternative(html_content, "text/html")

        # Attach image file safely
        file_path = Path(settings.BASE_DIR) / "image.png"
        email_message.attach_file(file_path)

        email_message.send(fail_silently=False)

        # form.save()

        # email = form.cleaned_data['email']
        # send_mail(subject="welcome to find my parking",message="Thank you for registering with Find My Parking.",from_email=settings.EMAIL_HOST_USER,recipient_list=[email])
        # form.save()
        return redirect('login') #error
      else:
        return render(request,'core/signup.html',{'form':form})  
    else:
        form = UserSignupForm()
        return render(request,'core/signup.html',{'form':form})
    

def userLoginView(request):
  if request.method =="POST":
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
      print(form.cleaned_data)
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = authenticate(request,email=email,password=password) #it will check in database..
      if user:
        login(request,user)
        if user.role == "admin":
          return redirect("admin_dashboard")
        elif user.role == "user":
          return redirect("user_dashboard")       
        elif user.role == "servicestaff":
          return redirect("servicestaff_dashboard")
    
      else:
        return redirect("login")
  
    else:
      return render(request,'core/login.html',{'form':form})  
    
  else:
    form = UserLoginForm()
    return render(request,'core/login.html',{'form':form})
  
def userLogoutView(request):
  logout(request)
  return redirect('home') 

