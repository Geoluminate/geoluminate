{% load i18n fairdm %}

{% blocktrans %}
### Paginated Literature List:
This response provides a paginated list of literature available within the database. It includes metadata about the pagination, such as the total count of literature entries, links to the next and previous pages if applicable, and an array of literature objects.

- `count`: Total count of literature entries available in the database.
- `next`: A link to the next page of literature entries. This field is nullable if there is no next page.
- `previous`: A link to the previous page of literature entries. This field is nullable if there is no previous page.
- `results`: An array containing literature objects.
{% endblocktrans %}
