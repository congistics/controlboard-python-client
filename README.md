# ControlBoard Python Client

This is python sdk for  [ControlBoard®](https://www.controlboard.app), the easiest-to-use, most powerful construction software on the market. The present version is a wrapper around the python graphql client and includes the ability to auto-refresh your access token for long-running integrations.

## Getting Started

## Getting a Client

Accessing the api requires the first part of your domain (customer.controlboard.app) and your client id and client secret. These are available to you in the admin section of ControlBoard under "Developer Credentials".

    from controlboard.client import get_controlboard_client
    from gql import gql

    client_id = '97ds97duid87d7d'
    client_secret = '23973uiuy338eujysuwyu8722'

    client = easy_client('customer', client_id, client_secret)
    query = gql(
        """
        {cxJobs { DisplayName }
        }

        """
    )
    res = client.execute(query)
    assert 'cxJobs' in res

The above simply returns all your jobs in ControlBoard.

You can also place the credentials in environment variables like so:

    ONTROLBOARD_DOMAIN=customer
    CONTROLBOARD_CLIENT_ID=97ds97duid87d7d
    CONTROLBOARD_CLIENT_SECRET=23973uiuy338eujysuwyu8722

In this case you can get a fully configured client like this:

    from controlboard.client import easy_client

    client = easy_client()



## Queries

The easiest way to figure out how to extract data from ControlBoard is by using the developer tools in the browser or by 