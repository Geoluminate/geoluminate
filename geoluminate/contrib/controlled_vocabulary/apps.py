from django.apps import AppConfig
from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def my_callback(
    app_config,
    verbosity=2,
    interactive=True,
    using=DEFAULT_DB_ALIAS,
    apps=global_apps,
    **kwargs,
):
    """
    Create content types for models in the given app.
    """
    from geoluminate.contrib.controlled_vocabulary.fields import ControlledVocabBase
    from geoluminate.contrib.controlled_vocabulary.models import ControlledVocabulary

    if not app_config.models_module:
        return

    try:
        # app_config = apps.get_app_config(app_label)
        apps.get_model("controlled_vocabulary", "ControlledVocabulary")
    except LookupError:
        return

    # get list of existing vocab labels
    labels = ControlledVocabulary.get_root_nodes().values_list("label", flat=True)

    for m in app_config.get_models():
        for f in m._meta.get_fields():
            # if the field is a ControlledVocabBase and the vocab_label is not in the list of existing labels
            if issubclass(type(f), ControlledVocabBase) and f.vocab_label not in labels:
                print(f"Adding {f.vocab_label} to ControlledVocabulary")
                ControlledVocabulary.add_root(label=f.vocab_label)


class ControlledVocabConfig(AppConfig):
    name = "geoluminate.contrib.controlled_vocabulary"
    label = "controlled_vocabulary"
    verbose_name = _("Controlled Vocabulary")

    def ready(self):
        post_migrate.connect(my_callback)
