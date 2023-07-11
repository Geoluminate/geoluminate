"""
These are the default settings for the commenting system built in to Geoluminate.
"""

# specify that we will use django-fluent-comments as our commenting application
COMMENTS_APP = "fluent_comments"
""""""


# --------- FLUENT COMMENTS SETTINGS --------- #

# AKISMET_API_KEY = None
# AKISMET_BLOG_URL = None
# AKISMET_IS_TEST = False


# FLUENT_COMMENTS_REPLACE_ADMIN = True

# Akismet spam fighting
# FLUENT_CONTENTS_USE_AKISMET = bool(AKISMET_API_KEY)
# FLUENT_COMMENTS_AKISMET_ACTION = 'soft_delete'

# Moderation
FLUENT_COMMENTS_DEFAULT_MODERATOR = "default"
""""""

# FLUENT_COMMENTS_CLOSE_AFTER_DAYS = None
# FLUENT_COMMENTS_MODERATE_BAD_WORDS = ()
# FLUENT_COMMENTS_MODERATE_AFTER_DAYS = None
# FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = True
# FLUENT_COMMENTS_MULTIPART_EMAILS = False

# Form layouts
# FLUENT_COMMENTS_FIELD_ORDER = ()
FLUENT_COMMENTS_EXCLUDE_FIELDS = ("name", "email", "url", "title")
""""""
FLUENT_COMMENTS_FORM_CLASS = "fluent_comments.forms.captcha.CompactLabelsCommentForm"
""""""
# FLUENT_COMMENTS_FORM_CSS_CLASS = 'comments-form form-horizontal'
# FLUENT_COMMENTS_LABEL_CSS_CLASS = 'col-sm-2'
# FLUENT_COMMENTS_FIELD_CSS_CLASS = 'col-sm-10'

# Compact style settings
# FLUENT_COMMENTS_COMPACT_FIELDS = ('name', 'email', 'url')
# FLUENT_COMMENTS_COMPACT_GRID_SIZE = 12
# FLUENT_COMMENTS_COMPACT_COLUMN_CSS_CLASS = "col-sm-{size}"
