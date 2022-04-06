from typing import Any, Dict

import requests

from .data import Method
from .exceptions import BugoutResponseException, BugoutUnexpectedResponse


def make_request(method: Method, url: str, **kwargs) -> Any:
    try:
        response = requests.request(method.value, url=url, **kwargs)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        response = err.response
        if not err.response:
            # Connection errors, timepouts, etc...
            raise BugoutResponseException("Network error", detail=str(err))
        if response.headers.get("Content-Type") == "application/json":
            exception_detail = response.json()["detail"]
        else:
            exception_detail = response.text
        raise BugoutResponseException(
            "An exception occurred at Bugout API side",
            status_code=response.status_code,
            detail=exception_detail,
        )
    except Exception as e:
        raise BugoutUnexpectedResponse({str(e)})
    return response.json()


def ping(url: str) -> Dict[str, Any]:
    url = f"{url.rstrip('/')}/ping"
    return make_request(Method.get, url)
