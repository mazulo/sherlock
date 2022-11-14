import sys
from concurrent.futures import Future
from typing import Any, Dict, List, Tuple, Union

import requests


def get_response(request_future: Future) -> Tuple[requests.Response, str]:
    # Default for Response object if some failure occurs
    response = None

    error_context = "General Unknown Error"
    try:
        response = request_future.result()
        if response.status_code:
            # Status code exists in response object
            error_context = None
    except requests.exceptions.HTTPError:
        error_context = "HTTP Error"
    except requests.exceptions.ProxyError:
        error_context = "Proxy Error"
    except requests.exceptions.ConnectionError:
        error_context = "Error Connecting"
    except requests.exceptions.Timeout:
        error_context = "Timeout Error"
    except requests.exceptions.RequestException:
        error_context = "Unknown Error"

    return response, error_context


def interpolate_string(target: Union[str, Dict, List], username: str) -> Union[str, Dict, List]:
    # Insert a string into the string properties of a target recursively

    if isinstance(target, str):
        return target.replace("{}", username)
    elif isinstance(target, dict):
        for key, value in target.items():
            target[key] = interpolate_string(value, username)
    elif isinstance(target, list):
        for i in target:
            target[i] = interpolate_string(target[i], username)

    return target


def check_for_parameter(username: str) -> bool:
    """
    Checks if {?} exists in the username
    if exist it means that sherlock is looking for more multiple username
    """
    return "{?}" in username


def multiple_usernames(username: str) -> List[str]:
    # Replace the parameter with symbols and return a list of usernames
    all_usernames = []
    check_symbols = ["_", "-", "."]

    for i in check_symbols:
        all_usernames.append(username.replace("{?}", i))
    return all_usernames


def timeout_check(value: str) -> float:
    """
    Check Timeout Argument

    Checks timeout for validity.

    Arguments:
    value                  -- Time in seconds to wait before timing out request.

    Return Value:
    Floating point number representing the time (in seconds) that should be
    used for the timeout.

    NOTE:  Will raise an exception if the timeout in invalid.
    """
    from argparse import ArgumentTypeError

    try:
        timeout = float(value)
    except Exception:
        raise ArgumentTypeError(f"Timeout '{value}' must be a number.")
    if timeout <= 0:
        raise ArgumentTypeError(f"Timeout '{value}' must be greater than 0.0s.")
    return timeout


def handler(signal_received: Any, frame: Any) -> None:
    """
    Exit gracefully without throwing errors

    Source: https://www.devdungeon.com/content/python-catch-sigint-ctrl-c
    """
    sys.exit(0)
