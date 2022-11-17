from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages  # import messages
from allauth.account.models import EmailAddress
from allauth.account.forms import AddEmailForm
from allauth.socialaccount.forms import DisconnectForm
from dashboard.dashboard import get_dashboard

User = get_user_model()


@login_required
def dashboard(request):
    context = dict(
        dashboard=get_dashboard('user'),
    )

    return render(request, 'dashboard/dashboard.html', context=context)


@login_required
def user_settings(request):
    context = dict(
        can_add_email=EmailAddress.objects.can_add_email(request.user),
        email_form=AddEmailForm(request),
        disconnect_form=DisconnectForm(request=request),
    )

    return render(request, 'user/account.html', context=context)


@login_required
def profile(request):
    context = dict(
        can_add_email=EmailAddress.objects.can_add_email(request.user),
        email_form=AddEmailForm(request),
        disconnect_form=DisconnectForm(request=request),
    )

    return render(request, 'dashboard/settings.html', context=context)


@login_required
def deactivate(request):
    context = {}
    try:
        user = User.objects.get(pk=request.user.pk)
        user.is_active = False
        user.save()
        context['msg'] = 'Profile successfully disabled.'
    except User.DoesNotExist:
        context['msg'] = 'User does not exist.'
    except Exception as e:
        context['msg'] = e.message

    return render(request, 'home.html', context=context)
