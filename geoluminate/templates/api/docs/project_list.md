{% load i18n geoluminate %}

{% blocktrans %}
### Paginated Project List:
This response provides a paginated list of projects available within the database. It includes metadata about the pagination, such as the total count of projects, links to the next and previous pages if applicable, and an array of project objects.

- `count`: Total count of projects available in the database.
- `next`: A link to the next page of projects. This field is nullable if there is no next page.
- `previous`: A link to the previous page of projects. This field is nullable if there is no previous page.
- `results`: An array containing project objects.
{% endblocktrans %}
