from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.conf import settings
from cryptography.fernet import Fernet
from django.core.mail import send_mail

# Create your views here.
def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            secret_key = settings.SECRET_KEY.encode()
            cipher_suite = Fernet(secret_key)


            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            user_key = cypher_suite.encrypt(username.encode()).decode()
            activation_link = settings.DOMAIN_URL+'/auth/email/activate/'+user_key


            send_mail(
                'confirm your account',
                f'click on {activation_link} to activate your account',
                settings.EMAIL_HOST_USER,
                [email,],
                fail_silently=True
            )

            messages.success(request, f'Activation Link send to your mail')
            return redirect('login')

    return render(request, 'users/register.html', {'form':form})

def confirm_mail(request, user_key):
    secret_key = settings.SECRET_KEY.encode()
    cipher_suite = Fernet(secret_key)
    user_key = user_key.encode()

    username = cipher_suite.decrypt(user_key).decode('utf-8')

    try:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()

        messages.success(request, 'Email is comfirmed')
        return redirect('login')
    except:
        messages.error(request, 'Invalid activation link')
        return redirect('login')
