# @pytest.mark.parametrize(
#     "name",
#     [
#         "available-extensions",
#         "detailed-index-usage",
#         "cache-hits",
#         "index-size",
#         "index-usage",
#         "sequence-usage",
#         "table-size",
#     ],
# )
# def test_postgres_metric_view(name, client, admin_client):
#     url = reverse("postgres-metrics:show", kwargs={"name": name})
#     response = admin_client.get(url)
#     assert response.status_code == 200
#     # make sure non-admin users cannot access
#     response = client.get(url)
#     assert response.status_code != 200


# def test_admin_erd_diagram(client, admin_client):
#     url = reverse("spaghetti:plate")
#     response = admin_client.get(url)
#     assert response.status_code == 200
#     # make sure non-admin users cannot access
#     response = client.get(url)
#     assert response.status_code != 200
