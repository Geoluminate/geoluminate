from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from allauth.account.views

User = get_user_model()

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
