{% load i18n fairdm %}

{% blocktrans %}
### Paginated Dataset List:
This response provides a paginated list of datasets available within the database. It includes metadata about the pagination, such as the total count of datasets, links to the next and previous pages if applicable, and an array of dataset objects.

- `count`: Total count of datasets available in the database.
- `next`: A link to the next page of datasets. This field is nullable if there is no next page.
- `previous`: A link to the previous page of datasets. This field is nullable if there is no previous page.
- `results`: An array containing dataset objects.
{% endblocktrans %}
