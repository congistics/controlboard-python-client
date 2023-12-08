import os
from dotenv import load_dotenv
from controlboard.client import make_test_client
from gql import gql


def test_minimal_client():
    load_dotenv()
    client = make_test_client()
    query = gql(
        """
        {cxJobs { DisplayName }
        }

        """
    )
    res = client.execute(query)
    assert 'cxJobs' in res
