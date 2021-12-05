from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# for email template
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")
            return redirect('login')


    form = UserRegisterForm()
    context = {}
    context['form'] = form
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)


        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, 'Your Profile has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    


    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)



def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data.get('email')
            user_mail = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Passwor Request'
                    email_template_name = 'users/password_message.txt'
                    parameters = {
                        'email': user.email,
                        'domain': '127.0.0.1',
                        'port': '8000',
                        'site_name': 'P_BLOG',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http'
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject,
                                email,
                                '',
                                [user.email],
                                fail_silently=False
                                )
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')

    else:
        password_form = PasswordResetForm()

    context = {
        'password_form': password_form
    }
    return render(request, 'users/password_reset.html', context)















# need install crispy and set for every forms in templates

# so'rash kerak forms.py da formalarni value lariga html classlarni  berish (widget?! or ...)

# pdf download for vs code shortcuts and download 2 video for fast productivity with vs code

# so'rash qachon biror profile ichida bo'lsa hello name turadi agar shu payt admin ga log parol qilib kirilsa page ham butunlay adminga o'tib qoladi? fix it



