from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import text_choices_factory


def inherited_choices_factory(name, *args):
    """Create a TextChoices class from an XMLSchema element."""
    cls_attrs = {}
    for choice_class in args:
        attrs = {a: getattr(choice_class, a) for a in vars(choice_class) if not a.startswith("_")}
        for key, choice in attrs.items():
            cls_attrs[key] = choice.value, choice.label

    return models.TextChoices(f"{name}Choices", cls_attrs)


class DateTimeChoices(models.TextChoices):
    """A class for storing choices for DateTimeField models. To use with fuzzy dates."""

    YEAR = "%Y", _("Year")
    MONTH = "%M", _("Month")
    DAY = "%d", _("Day")
    HOUR = "%h", _("Hour")
    MINUTE = "%m", _("Minute")
    SECOND = "%s", _("Second")


class ProjectStatus(models.IntegerChoices):
    CONCEPT = 0, _("Concept")
    PLANNING = 1, _("Planning")
    # SEARCHING_FOR_FUNDING = 3, _("Searching for funding")
    # SEARCHING_FOR_COLLABORATORS = 4, _("Searching for collaborators")
    IN_PROGRESS = 2, _("In progress")
    COMPLETE = 3, _("Complete")


# ================== DATACITE ROLES ==================
# https://support.datacite.org/docs/schema-43-attributes#section-contributor
# https://schema.datacite.org/meta/kernel-4.3/doc/DataCite-MetadataKernel_v4.3.pdf

# Datacite treat organisational and personal contributions in the same catergoy which ends up with a messy list of
# options that combines the two. We don't want to present a personal contributor with the option to select
# "HostingInstitution" or "ResearchGroup" as these are organisational roles. To overcome this, we have split the
# Datacite ContributorType vocabulary into three classes: PersonalRoles, OrganizationalRoles, and OtherRoles.

# Unfortunately, Django choices don't support inheritance, so we have to create a new class that inherits from
# all three classes. This is the ContributorRoles class. Text choices are also created for each class and stored on the
# Contributor model class for easy access in forms.


class PersonalRoles(models.TextChoices):
    """A class for storing choices for ContributorType on the Contributor model. Based on the
    Datacite ContributorType vocabulary."""

    CONTACT_PERSON = "ContactPerson", _("Contact Person")
    DATA_COLLECTOR = "DataCollector", _("Data Collector")
    DATA_CURATOR = "DataCurator", _("Data Curator")
    DATA_MANAGER = "DataManager", _("Data Manager")
    EDITOR = "Editor", _("Editor")
    PRODUCER = "Producer", _("Producer")
    RELATED_PERSON = "RelatedPerson", _("Related Person")
    RESEARCHER = "Researcher", _("Researcher")
    PROJECT_LEADER = "ProjectLeader", _("Project Leader")
    PROJECT_MANAGER = "ProjectManager", _("Project Manager")
    PROJECT_MEMBER = "ProjectMember", _("Project Member")
    SUPERVISOR = "Supervisor", _("Supervisor")
    WORK_PACKAGE_LEADER = "WorkPackageLeader", _("Work Package Leader")


class OrganizationalRoles(models.TextChoices):
    """A class for storing choices for ContributorType on the Contributor model. Based on the
    Datacite ContributorType vocabulary."""

    HOSTING_INSTITUTION = "HostingInstitution", _("Hosting Institution")
    RESEARCH_GROUP = "ResearchGroup", _("Research Group")
    SPONSOR = "Sponsor", _("Sponsor")


class OtherRoles(models.TextChoices):
    """A class for storing choices for ContributorType on the Contributor model. Based on the
    Datacite ContributorType vocabulary."""

    RIGHTS_HOLDER = "RightsHolder", _("Rights Holder")
    OTHER = "Other", _("Other")
    # DISTRIBUTOR = "Distributor", _("Distributor")


ContributorRoles = inherited_choices_factory("ContributorRole", PersonalRoles, OrganizationalRoles, OtherRoles)


class ProjectTags(models.TextChoices):
    """A class for storing choices for tags on the Project model."""

    COLLABORATORS_WANTED = "Collaborators wanted", _("Looking for collaborators")
    FUNDING_REQUIRED = "Funding required", _("Looking for funding")
    HAS_FUNDING = "Has funding", _("Has funding")
    POSITIONS_OPEN = "Positions open", _("Positions open")
    EQUIPMENT_REQUIRED = "Equipment required", _("Looking for tools")


ProjectTagss = [
    (
        _("Looking for"),
        [
            ("collaborators_wanted", _("Collaborators")),
            ("funding_wanted", _("Funding")),
            ("equipment_wanted", _("Equipment")),
        ],
    ),
    (
        _("Has"),
        [
            ("has_funding", _("Funding")),
            ("has_open_positions", _("Open Positions")),
            ("has_equipment", _("Equipment")),
        ],
    ),
]


iso_639_1_languages = [
    (
        "Common",
        [
            ("en", _("English")),
            ("es", _("Spanish")),
            ("fr", _("French")),
            ("de", _("German")),
            ("it", _("Italian")),
            ("pt", _("Portuguese")),
            ("ru", _("Russian")),
            ("zh", _("Chinese")),
            ("ja", _("Japanese")),
            ("ar", _("Arabic")),
        ],
    ),
    (
        "Other",
        [
            ("aa", _("Afar")),
            ("ab", _("Abkhazian")),
            ("ae", _("Avestan")),
            ("af", _("Afrikaans")),
            ("ak", _("Akan")),
            ("am", _("Amharic")),
            ("an", _("Aragonese")),
            # ("ar", _("Arabic")),
            ("as", _("Assamese")),
            ("av", _("Avaric")),
            ("ay", _("Aymara")),
            ("az", _("Azerbaijani")),
            ("ba", _("Bashkir")),
            ("be", _("Belarusian")),
            ("bg", _("Bulgarian")),
            ("bh", _("Bihari")),
            ("bi", _("Bislama")),
            ("bm", _("Bambara")),
            ("bn", _("Bengali")),
            ("bo", _("Tibetan")),
            ("br", _("Breton")),
            ("bs", _("Bosnian")),
            ("ca", _("Catalan")),
            ("ce", _("Chechen")),
            ("ch", _("Chamorro")),
            ("co", _("Corsican")),
            ("cr", _("Cree")),
            ("cs", _("Czech")),
            ("cu", _("Church Slavic")),
            ("cv", _("Chuvash")),
            ("cy", _("Welsh")),
            ("da", _("Danish")),
            # ("de", _("German")),
            ("dv", _("Divehi")),
            ("dz", _("Dzongkha")),
            ("ee", _("Ewe")),
            ("el", _("Greek")),
            # ("en", _("English")),
            ("eo", _("Esperanto")),
            # ("es", _("Spanish")),
            ("et", _("Estonian")),
            ("eu", _("Basque")),
            ("fa", _("Persian")),
            ("ff", _("Fulah")),
            ("fi", _("Finnish")),
            ("fj", _("Fijian")),
            ("fo", _("Faroese")),
            # ("fr", _("French")),
            ("fy", _("Western Frisian")),
            ("ga", _("Irish")),
            ("gd", _("Scottish Gaelic")),
            ("gl", _("Galician")),
            ("gn", _("Guarani")),
            ("gu", _("Gujarati")),
            ("gv", _("Manx")),
            ("ha", _("Hausa")),
            ("he", _("Hebrew")),
            ("hi", _("Hindi")),
            ("ho", _("Hiri Motu")),
            ("hr", _("Croatian")),
            ("ht", _("Haitian")),
            ("hu", _("Hungarian")),
            ("hy", _("Armenian")),
            ("hz", _("Herero")),
            ("ia", _("Interlingua")),
            ("id", _("Indonesian")),
            ("ie", _("Interlingue")),
            ("ig", _("Igbo")),
            ("ii", _("Sichuan Yi")),
            ("ik", _("Inupiaq")),
            ("io", _("Ido")),
            ("is", _("Icelandic")),
            # ("it", _("Italian")),
            ("iu", _("Inuktitut")),
            # ("ja", _("Japanese")),
            ("jv", _("Javanese")),
            ("ka", _("Georgian")),
            ("kg", _("Kongo")),
            ("ki", _("Kikuyu")),
            ("kj", _("Kwanyama")),
            ("kk", _("Kazakh")),
            ("kl", _("Kalaallisut")),
            ("km", _("Central Khmer")),
            ("kn", _("Kannada")),
            ("ko", _("Korean")),
            ("kr", _("Kanuri")),
            ("ks", _("Kashmiri")),
            ("ku", _("Kurdish")),
            ("kv", _("Komi")),
            ("kw", _("Cornish")),
            ("ky", _("Kirghiz")),
            ("la", _("Latin")),
            ("lb", _("Luxembourgish")),
            ("lg", _("Ganda")),
            ("li", _("Limburgan")),
            ("ln", _("Lingala")),
            ("lo", _("Lao")),
            ("lt", _("Lithuanian")),
            ("lu", _("Luba-Katanga")),
            ("lv", _("Latvian")),
            ("mg", _("Malagasy")),
            ("mh", _("Marshallese")),
            ("mi", _("Maori")),
            ("mk", _("Macedonian")),
            ("ml", _("Malayalam")),
            ("mn", _("Mongolian")),
            ("mr", _("Marathi")),
            ("ms", _("Malay")),
            ("mt", _("Maltese")),
            ("my", _("Burmese")),
            ("na", _("Nauru")),
            ("nb", _("Norwegian Bokmål")),
            ("nd", _("North Ndebele")),
            ("ne", _("Nepali")),
            ("ng", _("Ndonga")),
            ("nl", _("Dutch")),
            ("nn", _("Norwegian Nynorsk")),
            ("no", _("Norwegian")),
            ("nr", _("South Ndebele")),
            ("nv", _("Navajo")),
            ("ny", _("Chichewa")),
            ("oc", _("Occitan")),
            ("oj", _("Ojibwa")),
            ("om", _("Oromo")),
            ("or", _("Oriya")),
            ("os", _("Ossetian")),
            ("pa", _("Panjabi")),
            ("pi", _("Pali")),
            ("pl", _("Polish")),
            ("ps", _("Pashto")),
            # ("pt", _("Portuguese")),
            ("qu", _("Quechua")),
            ("rm", _("Romansh")),
            ("rn", _("Rundi")),
            ("ro", _("Romanian")),
            # ("ru", _("Russian")),
            ("rw", _("Kinyarwanda")),
            ("sa", _("Sanskrit")),
            ("sc", _("Sardinian")),
            ("sd", _("Sindhi")),
            ("se", _("Northern Sami")),
            ("sg", _("Sango")),
            ("si", _("Sinhala")),
            ("sk", _("Slovak")),
            ("sl", _("Slovenian")),
            ("sm", _("Samoan")),
            ("sn", _("Shona")),
            ("so", _("Somali")),
            ("sq", _("Albanian")),
            ("sr", _("Serbian")),
            ("ss", _("Swati")),
            ("st", _("Southern So")),
            ("su", _("Sundanese")),
            ("sv", _("Swedish")),
            ("sw", _("Swahili")),
            ("ta", _("Tamil")),
            ("te", _("Telugu")),
            ("tg", _("Tajik")),
            ("th", _("Thai")),
            ("ti", _("Tigrinya")),
            ("tk", _("Turkmen")),
            ("tl", _("Tagalog")),
            ("tn", _("Tswana")),
            ("to", _("Tonga")),
            ("tr", _("Turkish")),
            ("ts", _("Tsonga")),
            ("tt", _("Tatar")),
            ("tw", _("Twi")),
            ("ty", _("Tahitian")),
            ("ug", _("Uighur")),
            ("uk", _("Ukrainian")),
            ("ur", _("Urdu")),
            ("uz", _("Uzbek")),
            ("ve", _("Venda")),
            ("vi", _("Vietnamese")),
            ("vo", _("Volapük")),
            ("wa", _("Walloon")),
            ("wo", _("Wolof")),
            ("xh", _("Xhosa")),
            ("yi", _("Yiddish")),
            ("yo", _("Yoruba")),
            ("za", _("Zhuang")),
            # ("zh", _("Chinese")),
            ("zu", _("Zulu")),
        ],
    ),
]
