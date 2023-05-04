import logging
from os.path import realpath

from django.core.management import call_command
from django.http import Http404
from django.shortcuts import redirect
from django.urls.exceptions import NoReverseMatch
from django.utils.functional import cached_property
from django.views.generic import TemplateView
from polib import pofile
from rosetta import get_version as get_rosetta_version
from rosetta import views
from rosetta.access import can_translate_language
from rosetta.conf import settings as rosetta_settings
from rosetta.poutil import find_pos

logger = logging.getLogger(__name__)


class BaseMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["languages"] = self.get_project_languages()
        return context

    def get_project_paths(self, lang_code):
        return self._get_paths(lang_code, True)

    def get_project_files(self, lang_code):
        return self._get_files(self.get_project_paths(lang_code))

    def get_all_paths(self, lang_code):
        return self._get_paths(lang_code)

    def get_all_files(self, lang_code):
        return self._get_files(self.get_all_paths(lang_code))

    def _get_paths(self, lang_code, project=False):
        if project:
            return find_pos(lang_code, True)
        return find_pos(lang_code, True, True, True)

    def _get_files(self, path_list):
        return [(views.get_app_name(lang), realpath(lang), pofile(lang)) for lang in path_list]

    def get_project_languages(self):
        """Gets a dictionary of all languages that have been generated for the
        current project.
        """
        proj_languages = {}
        for code, language in rosetta_settings.ROSETTA_LANGUAGES:
            paths = self.get_project_paths(code)

            # if a path exists in the project for the given language
            # AND the user has permission
            if paths and can_translate_language(self.request.user, code):
                proj_languages[code] = {
                    "name": language,
                }

        return proj_languages

    def get_progress(self, code, project_only=True):
        paths = self._get_paths(code, project_only)
        files = self._get_files(paths)
        progress = [x[2].percent_translated() for x in files]
        if progress:
            return sum(progress) / len(progress)
        else:
            return 0

    def app_path_dict(self, lang_code):
        paths = self.get_all_paths(lang_code)
        return {views.get_app_name(path): path for path in paths}

    @property
    def lang_code(self):
        return self.kwargs.get("lang_id")

    @property
    def app_name(self):
        return self.kwargs.get("app_name")

    @property
    def lang_dict(self):
        return dict(rosetta_settings.ROSETTA_LANGUAGES)

    @property
    def lang_name(self):
        return self.lang_dict.get(self.lang_code)


class TranslationIndexView(BaseMixin, views.RosettaBaseMixin, TemplateView):
    template_name = "jazzmin_translate/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for code in context["languages"]:
            context["languages"][code].update(
                applications=self.get_all_files(code),
                progress=self.get_progress(code),
                total_progress=self.get_progress(code, project_only=False),
            )
        sorted(context["languages"].items(), key=lambda x: (x[1]["name"]))
        context["version"] = get_rosetta_version()
        return context


class LanguageView(BaseMixin, views.RosettaBaseMixin, TemplateView):
    template_name = "jazzmin_translate/language.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (
            self.lang_code not in self.lang_dict.keys()
            or can_translate_language(self.request.user, self.lang_code) is False
        ):
            raise Http404

        po_files = self.get_all_files(self.lang_code)
        po_files.sort(key=lambda app: (app[2].percent_translated(), app[0]))

        context["lang_code"] = self.lang_code
        context["language"] = self.lang_name
        context["pos"] = po_files
        context["version"] = get_rosetta_version()
        return context

    # @property
    # def language(self):
    #     return self.kwargs.get("lang_id")

    # @cached_property
    # def po_filter(self):
    #     return "all"


class ApplicationView(BaseMixin, views.TranslationFormView):
    template_name = "jazzmin_translate/application.html"

    def post(self, request, *args, **kwargs):
        # The TranslationFormView superclass redirects to the rosetta
        # form view which raises a NoReverseMatch exception if the rosetta urls
        # are not included. We will let the rosetta post method do it's thing,
        # catch the exception, then redirect to our own view.
        try:
            super().post(request, *args, **kwargs)
        except NoReverseMatch:
            return redirect("geoluminate_admin.application", **self.kwargs)

    @cached_property
    def po_file_path(self):
        """Based on the url kwargs, infer and return the path to the .po file to
        be shown/updated.

        Throw a 404 if a file isn't found.
        """

        path_dict = self.app_path_dict(self.language_id)
        try:
            return path_dict[self.app_name]
        except KeyError:
            logger.exception("Could not find the specified application.")
            return Http404


def create_locale_file(request, lang_id):
    logger.info(f"Creating file for {lang_id}")
    call_command("makemessages", "-l", lang_id)
    return redirect("jazzmin_translate.index")
