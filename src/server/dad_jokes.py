import math

import requests
from requests import HTTPError

I_CAN_HAZ_DAD_JOKES_API_URL = "https://icanhazdadjoke.com/search"
MAX_JOKE_REQUEST_SIZE = 30


def fetch_jokes(api_endpoint_url, count=100, current_page=1):
    results = []

    n_requests = math.floor(count / MAX_JOKE_REQUEST_SIZE)
    n_requests += 1 if count % MAX_JOKE_REQUEST_SIZE > 0 else 0
    print(n_requests)

    for i in range(n_requests):
        limit = count % MAX_JOKE_REQUEST_SIZE if i == n_requests else MAX_JOKE_REQUEST_SIZE
        try:
            response = requests.get(
                url=api_endpoint_url,
                headers={
                    "Accept": "application/json"
                },
                params={
                    "limit": limit,
                    "page": current_page
                }
            )
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        else:
            results.append(response.json())
            current_page += 1

    return results
