import pytest
from django.urls import reverse
from rest_framework import status
# HI I DID IT?????
@pytest.mark.django_db
def test_api_app_status(client):
    # URL for the api_app endpoint (you can replace this with the correct URL pattern if needed)
    url = '/api_app/'  # Adjust this to the actual endpoint if needed

    # Send a GET request to the URL
    response = client.get(url)

    # Assert that the status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

