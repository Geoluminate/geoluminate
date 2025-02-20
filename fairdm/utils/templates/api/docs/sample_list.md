{% load i18n fairdm %}

{% blocktrans %}
### Paginated Sample List:
This response provides a paginated list of samples available within the database. It includes metadata about the pagination, such as the total count of samples, links to the next and previous pages if applicable, and an array of sample objects.

- `count`: Total count of samples available in the database.
- `next`: A link to the next page of samples. This field is nullable if there is no next page.
- `previous`: A link to the previous page of samples. This field is nullable if there is no previous page.
- `results`: An array containing sample objects.
{% endblocktrans %}
