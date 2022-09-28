from allauth.account.adapter import DefaultAccountAdapter
from django.http import JsonResponse
from django.shortcuts import render
from crispy_forms.utils import render_crispy_form
from django.template.context_processors import csrf
from django.contrib import messages
from django.template.loader import render_to_string

class AuthenticationAdapter(DefaultAccountAdapter):

    # def respond_email_verification_sent(self, request, user):
        # return HttpResponseRedirect("/")

    def ajax_response(self, request, response, redirect_to=None, form=None, data=None):
        resp = {}
        status = response.status_code

        if redirect_to:
            status = 200
            # resp["location"] = redirect_to
        if form:
            if request.method == "POST":
                if form.is_valid():
                    status = 200
                    self.add_message(request, messages.SUCCESS, "account/messages/email_confirmation_resend.txt")

                    resp['html'] = render_to_string("authentication/components/form_success.html", {'messages': messages.get_messages(request)}).strip()
                else:
                    status = 400
                    resp['form'] = render_crispy_form(form, context=csrf(request))
            else:
                status = 200
        return JsonResponse(resp, status=status)
