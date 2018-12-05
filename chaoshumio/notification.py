# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import platform
from typing import Any, Dict

from chaoslib.types import EventPayload
from logzero import logger
import requests


__all__ = ["notify"]


def notify(settings: Dict[str, Any], event: EventPayload):
    """
    Send a log message to the Humio ingest endpoint.

    The settings must contain:

    - `"token"`: a slack API token
    - `"url"`: the channel where to send this event notification

    If one of these two attributes is missing, no notification is sent.

    """

    token = settings.get("token")
    dataspace = settings.get("dataspace")
    isotimestamp = datetime.fromtimestamp(
        event["ts"], timezone.utc).isoformat()

    if not token:
        logger.debug("Humio notifier requires a token")
        return

    if not dataspace:
        logger.debug("Humio notifier requires a dataspace")
        return

    token = token.strip()
    dataspace = dataspace.strip()
    url = "https://cloud.humio.com/api/v1/dataspaces/{}/ingest".format(
        dataspace)

    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }

    host = platform.node()
    payload = [{
        "tags": {
            "host": host,
            "platform": platform.platform(),
            "python": platform.python_version(),
            "system": platform.system(),
            "machine": platform.machine(),
            "provider": "chaostoolkit",
            "chaosengineering": "true"
        },
        "events": [
            {
                "timestamp": isotimestamp,
                "attributes": event["payload"]
            },
        ]
    }]

    r = requests.post(url, headers=headers, json=payload, timeout=(2, 10))
    if r.status_code > 399:
        logger.debug(
            "Failed to post to Humio with status code of {status} with"
            " reason: {reason}".format(status=r.status_code, reason=r.text))
