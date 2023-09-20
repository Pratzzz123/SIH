
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import SmartUrja
from cyberRakshak import settings
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import  HttpResponse
from .utils import getIP
from .models import SmartUrja
# Create your views here.

def main(request):
    return render(request, 'main.html')

def submit(request):
    if request.method == "POST":
        
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(username = username, password = pwd)
        # myuser = SmartUrja(username = username, password = pwd, email = email)
        # myuser.save()
        if not User.objects.filter(email=email).exists():
             return render(request, 'main.html', {'error': "Wrong credentials"})
            # return redirect('main')
        if not username.isalnum():
             return render(request, 'main.html', {'error': "username should be alphanumeric"})
        if user.is_active is None:
            return render(request, 'main.html', {'error': "Verify e-mail"})
        if user is not None:
            
            login(request, user)
            user.is_active = False
            user.save()
            currentIP = getIP()
            subject = "recent login detected"
            message2 = render_to_string('email_confirmation.html', {
                'name': user.username, 
                'domain': (get_current_site(request)).domain, 
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
                })
            email = EmailMessage(
                subject,
                message2,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()
            return render(request, 'submit.html', {'username': username})
        else:
            return render(request, 'main.html', {'error': "Wrong credentials"})
        # return render(request, 'submit.html', {'username': username})
    # return render(request, 'submit.html', {})

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('main')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_encode(uidb64))
        user = User.objects.get(User, pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('submit', {'username': user.username, 'confirmed': "confirmed"})
    else:
        return render(request, 'fail.html')
    
# print(getIP())
