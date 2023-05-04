import datetime
import ipaddress

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.urls import Resolver404, resolve
from lockdown import middleware

from geoluminate.models import GlobalConfiguration


class GeoluminateLockdownMiddleware(middleware.LockdownMiddleware):
    """Middleware to lock down a Geoluminate project."""

    # pylint: disable=too-many-locals,too-many-return-statements
    # pylint: disable=too-many-statements,too-many-branches
    def process_request(self, request):
        """Check if each request is allowed to access the current resource."""

        self.config = GlobalConfiguration.get_solo()
        session = self.get_session(request)
        form = self.get_form(request)

        if any(
            [
                # lock down has not enabled
                not self.sitewide_lockdown(),
                # Don't lock down if the client REMOTE_ADDR matched and is part of the
                # exception list.
                self.remote_addr_matches_exception_list(request),
                self.url_matches_lockdown_exception_pattern(request),
                # Don't lock down if outside of the lockdown dates.
                self.lockdown_dates_not_applicable(),
                self.view_is_whitelisted(request),
                self.user_already_authorized(form, session, request),
            ]
        ):
            return None

        if form.is_valid():
            token = form.generate_token() if hasattr(form, "generate_token") else True
            session[self.session_key] = token
            return self.redirect(request)

        return render(request, "lockdown/form.html", self.get_context_data(form))

    def get_context_data(self, form):
        page_data = {}
        if not hasattr(form, "show_form") or form.show_form():
            page_data["form"] = form

        if self.extra_context:
            page_data.update(self.extra_context)

        return page_data

    def get_session(self, request):
        try:
            return request.session
        except AttributeError as exc:
            raise ImproperlyConfigured("django-lockdown requires the Django sessions framework") from exc

    def get_form(self, request):
        form_data = request.POST if request.method == "POST" else None
        if self.form:
            form_class = self.form
        else:
            form_class = middleware.get_lockdown_form(getattr(settings, "LOCKDOWN_FORM", "lockdown.forms.LockdownForm"))
        return form_class(data=form_data, **self.form_kwargs)

    def lockdown_dates_not_applicable(self):
        until_date = self.until_date if self.until_date else getattr(settings, "LOCKDOWN_UNTIL_DATE", None)

        after_date = self.after_date if self.after_date else getattr(settings, "LOCKDOWN_AFTER_DATE", None)

        if until_date or after_date:
            locked_date = False
            if until_date and datetime.datetime.now() < until_date:
                locked_date = True
            if after_date and datetime.datetime.now() > after_date:
                locked_date = True
            if not locked_date:
                return None

    def remote_addr_matches_exception_list(self, request):
        """Returns True if the client REMOTE_ADDR matches an entry from the
        `LOCKDOWN_REMOTE_ADDR_EXCEPTIONS` exception list.
        """

        if self.remote_addr_exceptions:
            remote_addr_exceptions = self.remote_addr_exceptions
        else:
            remote_addr_exceptions = getattr(settings, "LOCKDOWN_REMOTE_ADDR_EXCEPTIONS", [])

        # remote_addr_exceptions = self.config.remote_addr_exceptions

        remote_addr_exceptions = [ipaddress.ip_network(ip) for ip in remote_addr_exceptions]
        if remote_addr_exceptions:
            # If forwarding proxies are used they must be listed as trusted
            # trusted_proxies = self.config.trusted_proxies

            trusted_proxies = self.trusted_proxies or getattr(settings, "LOCKDOWN_TRUSTED_PROXIES", [])
            trusted_proxies = [ipaddress.ip_network(ip) for ip in trusted_proxies]

            remote_addr = ipaddress.ip_address(request.META.get("REMOTE_ADDR"))
            if any(remote_addr for ip_exceptions in remote_addr_exceptions if remote_addr in ip_exceptions):
                return True

            if any(remote_addr for proxy in trusted_proxies if remote_addr in proxy):
                # If REMOTE_ADDR is a trusted proxy check x-forwarded-for
                x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
                if x_forwarded_for:
                    remote_addr = ipaddress.ip_address(x_forwarded_for.split(",")[-1].strip())
                    if any(remote_addr for ip_exceptions in remote_addr_exceptions if remote_addr in ip_exceptions):
                        return True

    def url_matches_lockdown_exception_pattern(self, request):
        # Don't lock down if the URL matches an exception pattern.

        if self.url_exceptions:
            url_exceptions = middleware.compile_url_exceptions(self.url_exceptions)
        else:
            url_exceptions = middleware.compile_url_exceptions(getattr(settings, "LOCKDOWN_URL_EXCEPTIONS", ()))
        for pattern in url_exceptions:
            if pattern.search(request.path):
                return True

    def view_is_whitelisted(self, request):
        # Don't lock down if the URL resolves to a whitelisted view.
        try:
            resolved_path = resolve(request.path)
        except Resolver404:
            pass
        else:
            if resolved_path.func in getattr(settings, "LOCKDOWN_VIEW_EXCEPTIONS", []):
                return True

    def user_already_authorized(self, form, session, request):
        authorized = False
        token = session.get(self.session_key)
        if hasattr(form, "authenticate"):
            if form.authenticate(token):
                authorized = True
        elif token is True:
            authorized = True

        if authorized and self.logout_key and self.logout_key in request.GET:
            if self.session_key in session:
                del session[self.session_key]
            querystring = request.GET.copy()
            del querystring[self.logout_key]
            return self.redirect(request)

        # Don't lock down if the user is already authorized for previewing.
        if authorized:
            return True

    def sitewide_lockdown(self):
        # settings.LOCKDOWN_ENABLED is prioritized over config.lockdown_enabled
        # so that devs can can lock down the site for staging without being
        # overridden by admin

        # if getattr(settings, "LOCKDOWN_ENABLED") is False:
        #     return True

        if self.config.lockdown_enabled:
            return True
