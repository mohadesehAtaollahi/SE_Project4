from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from detector.models import *
from django.contrib.auth import update_session_auth_hash
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import UserSecurity, PasswordResetToken


def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request,user)
        return redirect("profile")

    return render(request,"register.html",{"form":form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )

        if user:
            login(request,user)
            return redirect("profile")

    return render(request,"login.html",{"form":form})


def logout_view(request):
    logout(request)
    return redirect("/")



@login_required
def profile_view(request):
    try:
        gender_result = GenderDetectionResult.objects.get(user=request.user)
        has_results = True
    except GenderDetectionResult.DoesNotExist:
        gender_result = None
        has_results = False

    all_results = GenderDetectionResult.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'user': request.user,
        'gender_result': gender_result,
        'has_results': has_results,
        'all_results': all_results,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    })

    return render(request,"profile.html")


#########part2##########

def password_reset_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
            try:
                user_security = UserSecurity.objects.get(user=user)
                request.session['reset_username'] = username
                request.session['reset_user_id'] = user.id
                return redirect('security_question')
            except UserSecurity.DoesNotExist:
                messages.error(request, 'No security question found for this user.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'password_reset_start.html')


def security_question_view(request):
    username = request.session.get('reset_username')
    user_id = request.session.get('reset_user_id')

    if not username or not user_id:
        return redirect('password_reset_request')

    try:
        user = User.objects.get(id=user_id, username=username)
        user_security = UserSecurity.objects.get(user=user)

        if request.method == 'POST':
            user_answer = request.POST.get('answer')

            if user_security.verify_answer(user_answer):
                reset_code = get_random_string(6, '0123456789')

                PasswordResetToken.objects.create(
                    user=user,
                    token=reset_code,
                    expires_at=timezone.now() + timedelta(minutes=10)
                )

                request.session['reset_code'] = reset_code

                return render(request, 'show_reset_code.html', {
                    'reset_code': reset_code,
                    'user': user,
                    'expiry_time': timezone.now() + timedelta(minutes=10)
                })
            else:
                messages.error(request, 'Incorrect answer. Please try again.')

        return render(request, 'security_question.html', {
            'question': user_security.get_question_display(),
            'username': username
        })

    except (User.DoesNotExist, UserSecurity.DoesNotExist):
        messages.error(request, 'Error processing your request.')
        return redirect('password_reset_request')


def show_reset_code(request):
    reset_code = request.session.get('reset_code')
    username = request.session.get('reset_username')

    if not reset_code or not username:
        from django.contrib import messages
        messages.error(request, 'Please start the password reset process from the beginning.')
        from django.shortcuts import redirect
        return redirect('password_reset_request')

    expiry_time = timezone.now() + timedelta(minutes=10)

    context = {
        'reset_code': reset_code,
        'username': username,
        'expiry_time': expiry_time
    }

    return render(request, 'registration/show_reset_code.html', context)
def enter_reset_code(request):
    reset_code = request.session.get('reset_code')
    user_id = request.session.get('reset_user_id')

    if not reset_code or not user_id:
        messages.error(request, 'Please start the password reset process from the beginning.')
        return redirect('password_reset_request')

    if request.method == 'POST':
        entered_code = request.POST.get('reset_code')

        if entered_code == reset_code:
            return redirect('set_new_password')
        else:
            messages.error(request, 'Invalid reset code. Please try again.')

    return render(request, 'enter_reset_code.html')


def set_new_password(request):
    reset_code = request.session.get('reset_code')
    user_id = request.session.get('reset_user_id')

    if not reset_code or not user_id:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('password_reset_request')

    try:
        user = User.objects.get(id=user_id)

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
            else:
                user.set_password(new_password)
                user.save()

                try:
                    reset_token = PasswordResetToken.objects.get(
                        token=reset_code,
                        user=user,
                        is_used=False
                    )
                    reset_token.is_used = True
                    reset_token.save()
                except PasswordResetToken.DoesNotExist:
                    pass

                request.session.pop('reset_username', None)
                request.session.pop('reset_user_id', None)
                request.session.pop('reset_code', None)

                login(request, user)

                messages.success(request, 'Your password has been changed successfully!')
                return redirect('home')

        return render(request, 'set_new_password.html', {
            'username': user.username
        })

    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('password_reset_request')


def reset_with_token(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(
            token=token,
            is_used=False
        )

        if not reset_token.is_valid():
            return render(request, 'token_expired.html')

        request.session['reset_code'] = token
        request.session['reset_user_id'] = reset_token.user.id

        return redirect('set_new_password')

    except PasswordResetToken.DoesNotExist:
        return render(request, 'registration/invalid_token.html')


@login_required
def change_password_view(request):

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        errors = []

        if not request.user.check_password(current_password):
            errors.append('Current password is incorrect.')
        if new_password != confirm_password:
            errors.append('New passwords do not match.')
        if len(new_password) < 8:
            errors.append('New password must be at least 8 characters.')

        if current_password == new_password:
            errors.append('New password must be different from current password.')

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)

            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile')

    return render(request, 'change_password.html')
