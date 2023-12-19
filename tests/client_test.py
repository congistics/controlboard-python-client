from dotenv import load_dotenv
from controlboard.client import easy_client
from gql import gql


def test_minimal_client():
    load_dotenv()
    client = easy_client()
    query = gql(
        """
        {cxJobs { DisplayName }
        }

        """
    )
    res = client.execute(query)
    assert 'cxJobs' in res
