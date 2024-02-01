"""Contains security settings for the project."""

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
# X_FRAME_OPTIONS = "DENY"
X_FRAME_OPTIONS = "SAMEORIGIN"


# TEXT FIELD BLEACHING

# https://bleach.readthedocs.io/en/latest/clean.html#bleach.clean
# https://github.com/marksweb/django-bleach

# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS = ["p", "b", "i", "u", "em", "strong", "a"]

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = ["href", "title", "style"]

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = ["font-family", "font-weight", "text-decoration", "font-variant"]

# Strip unknown tags if True, replace with HTML escaped characters if
# False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = True

# BLEACH_DEFAULT_WIDGET = "formset.richtext.widgets.RichTextarea"
# BLEACH_DEFAULT_WIDGET = "djangocms_text_ckeditor.widgets.TextEditorWidget"
