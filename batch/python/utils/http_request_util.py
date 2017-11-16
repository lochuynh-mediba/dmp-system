import requests


def http_get_request_json(url, params=None, auth=None):
    """
    get request from url, return json data

    Parameters
    ----------
    url                 : String
            url to get request
    params              : Dict
            parameters
    auth                : requests.auth
            authentication

    Examples
    --------

    Returns
    -------
    json                : json data
            json content if status_code = 200
            other status code will raise exceptions
    """
    response = requests.get(url, timeout=10, params=params, auth=auth)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def http_get_request_content_string(url, params=None, timeout=60, auth=None):
    """
    get request from url, return content data in string

    Parameters
    ----------
    url                 : String
            url to get request
    params              : Dict
            parameters
    timeout             : int
            timeout
    auth                : requests.auth
            authentication

    Examples
    --------

    Returns
    -------
    response_content    : str
            string response content
            other status code will raise exceptions
    """
    response = requests.get(url, timeout=timeout, params=params, auth=auth)

    if response.status_code != 200:
        response.raise_for_status()

    response_content = response.content.decode('ascii')
    return response_content

