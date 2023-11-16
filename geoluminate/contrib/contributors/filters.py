import django_filters as df

from .models import Contribution, Contributor


class ContributorFilter(df.FilterSet):
    class Meta:
        model = Contributor
        fields = {
            "type": ["exact"],
            "name": ["icontains"],
        }


class ContributionFilter(df.FilterSet):
    class Meta:
        model = Contribution
        fields = {
            "roles": ["icontains"],
        }
