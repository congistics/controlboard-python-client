import os
import requests
from gql.transport.exceptions import TransportServerError
from requests.auth import HTTPBasicAuth
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


def create_refresh_token_func(domain, client_id, client_secret):
    """
    Create a function to refresh the authentication token.

    :param domain: The domain for the authentication server.
    :param client_id: The client ID for authentication.
    :param client_secret: The client secret for authentication.
    :return: A function that, when called, returns a refreshed authentication token.
    """

    def refresh_token():
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials'
        }

        response = requests.post(
            f'https://cbd-{domain}-api.auth.us-east-1.amazoncognito.com/oauth2/token'
            , auth=HTTPBasicAuth(client_id, client_secret), data=data, headers=headers)
        response.raise_for_status()
        return response.json()['access_token']

    return refresh_token


def get_controlboard_client(domain, client_id, client_secret):
    """
    Create a GraphQL client wrapper that handles token refresh and transport recreation.

    :param domain: The domain for the authentication server.
    :param client_id: The client ID for authentication.
    :param client_secret: The client secret for authentication.
    :return: A wrapped GraphQL client.
    """

    def create_transport(domain, token):
        """ Create a transport layer for the GraphQL client. """
        return AIOHTTPTransport(url=f"https://{domain}.controlboard.app/graphql", headers={'Authorization': token})

    def create_client(transport):
        """ Create a GraphQL client with the given transport. """
        return Client(transport=transport, fetch_schema_from_transport=True)

    def method_wrapper(name):
        def wrapped(*args, **kwargs):
            try:
                return getattr(client, name)(*args, **kwargs)
            except TransportServerError as e:
                print(f"An error occurred: {e}. Attempting to refresh token and recreate transport.")
                if e.code == 401:
                    client.transport = create_transport(domain, refresh_token())
                    return getattr(client, name)(*args, **kwargs)
                raise e
        return wrapped

    class ControlBoardClient:
        def __getattr__(self, item):
            if callable(getattr(client, item, None)):
                return method_wrapper(item)
            return getattr(client, item)

    refresh_token = create_refresh_token_func(domain, client_id, client_secret)
    initial_transport = create_transport(domain, refresh_token())
    client = create_client(initial_transport)

    return ControlBoardClient()

def make_test_client():
    return get_controlboard_client(
        os.getenv('CONTROLBOARD_DOMAIN'),
        os.getenv('CONTROLBOARD_CLIENT_ID'),
        os.getenv('CONTROLBOARD_CLIENT_SECRET')
    )

