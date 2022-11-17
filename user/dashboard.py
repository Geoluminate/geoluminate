from dashboard.dashboard import Dashboard, App
from django.utils.translation import gettext_lazy as _


class UserDashboard(Dashboard):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children = [
            App(_('Account'), 'user:settings', icon='fa-user'),
            # App(_('Projects'), 'user:projects', icon='fa-user'),
            # App(_('Publications'), 'user:publications', icon='fa-user'),
            # App(_('Reviews'),
            #     'review:user_review_list',
            #     icon='fa-search-location'),
        ]
