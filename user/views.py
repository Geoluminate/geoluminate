from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages  # import messages
from allauth.account.models import EmailAddress
from allauth.account.forms import AddEmailForm
from allauth.socialaccount.forms import DisconnectForm, SignupForm
from geoluminate.dashboard import get_dashboard
from django.utils.translation import gettext as _
from allauth.socialaccount.views import ConnectionsView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

User = get_user_model()


@login_required
def dashboard(request):
    context = dict(
        dashboard=get_dashboard('user'),
    )

    return render(request, 'user/dashboard.html', context=context)


class Account(LoginRequiredMixin, TemplateView):
    template_name = 'user/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_email'] = EmailAddress.objects.can_add_email(
            self.request.user)
        context['forms'] = [
            (_('E-mail Addresses'),
             "account/email.html",
             AddEmailForm(self.request)),
            (_('Password Reset'),
             "account/password_reset.html",
             DisconnectForm(request=self.request)),
            (_('Account Connections'),
             "socialaccount/connections.html",
             AddEmailForm(self.request)),
        ]
        return context


@login_required
def user_settings(request):
    context = dict()

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
