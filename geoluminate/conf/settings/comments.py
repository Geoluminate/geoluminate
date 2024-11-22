"""
Default settings for the commenting system built in to Geoluminate.
"""

COMMENTS_APP = "django_comments_xtd"

COMMENTS_XTD_THREADED_EMAILS = True
COMMENTS_XTD_MAX_THREAD_LEVEL = 8  # Maximum thread level for comments
COMMENTS_XTD_API_GET_USER_AVATAR = "geoluminate.contrib.contributors.utils.get_avatar_url"
# COMMENTS_XTD_LIST_ORDER = ("-thread_id", "order")  # Default comment ordering
COMMENTS_XTD_APP_MODEL_OPTIONS = {
    "default": {"allow_flagging": True, "allow_feedback": True, "show_feedback": True, "who_can_post": "users"}
}

#  To help obfuscating comments before they are sent for confirmation.
COMMENTS_XTD_SALT = b"Timendi causa est nescire. " b"Aequam memento rebus in arduis servare mentem."

# Optional: Email settings for comment notifications
COMMENTS_XTD_FROM_EMAIL = "no-reply@example.com"
COMMENTS_XTD_CONTACT_EMAIL = "admin@example.com"
