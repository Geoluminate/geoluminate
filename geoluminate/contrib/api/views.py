from django.views.generic import TemplateView


class TOSView(TemplateView):
    template_name = "geoluminate/generic/api/tos.html"
