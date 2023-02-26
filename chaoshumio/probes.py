from typing import Any, Dict, Optional, Union

import requests
from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

__all__ = ["search_query"]
BASE_HUMIO_URL = "https://cloud.humio.com"


def search_query(
    qs: str,
    start: Union[int, str] = "24hours",
    end: Union[int, str] = "now",
    tz_offset: int = 0,
    params: Optional[Union[str, Dict[str, str]]] = None,
    result_as_text: Optional[bool] = False,
    configuration: Optional[Configuration] = None,
    secrets: Optional[Secrets] = None,
) -> Any:
    """
    Perform a search query against the Humio API and returns its result as-is.

    Set `result_as_text` to `true` to get the result as a raw string, otherwise
    the probe returns a JSON payload.

    Make sure to set the Humio token as part of the experiment secrets and
    the repository name as part of its configuration section using the
    `humio_repository` key.

    See https://docs.humio.com/api/using-the-search-api-with-humio/#query
    """
    token = (secrets or {}).get("token", "").strip()
    if not token:
        logger.debug("Missing Humio token secret")
        raise ActivityFailed(
            "Missing the Humio token from secrets, please set one."
        )

    configuration = configuration or {}
    repo_name = configuration.get("humio_repository", "sandbox")
    if not repo_name:
        raise ActivityFailed(
            "Missing the Humio repository name from the configuration, "
            "please set one as `humio_repository`."
        )

    payload = {"queryString": qs}  # type: Dict[str, Any]

    if start:
        payload["start"] = start

    if end:
        payload["end"] = end

    if tz_offset:
        payload["timeZoneOffsetMinutes"] = tz_offset

    if params:
        payload["arguments"] = params

    humio_url = configuration.get("humio_url", BASE_HUMIO_URL).strip()
    humio_url = "{}/api/v1/repositories/{}/query".format(
        humio_url, repo_name.strip()
    )
    logger.debug("Searching Humio at '{}'".format(humio_url))

    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
        "Accept": "text/plain" if result_as_text else "application/json",
    }

    r = requests.post(humio_url, headers=headers, json=payload)
    if r.status_code > 399:
        logger.debug(
            "Failed to query Humio with status code of {status} with"
            " reason: {reason}".format(status=r.status_code, reason=r.text)
        )
        raise ActivityFailed(
            "Failed to run search query against Humio: {}".format(r.text)
        )

    if r.headers["content-type"] == "text/plain":
        return r.text

    return r.json()
