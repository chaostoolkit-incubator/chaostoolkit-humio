# -*- coding: utf-8 -*-
import platform
from datetime import datetime, timezone
from typing import Any, Dict

import requests
from chaoslib.types import EventPayload
from logzero import logger

__all__ = ["notify"]


def notify(settings: Dict[str, Any], event: EventPayload) -> None:
    """
    Send a log message to the Humio ingest endpoint.

    The settings must contain:

    - `"token"`: a slack API token
    - `"humio_url"`: the Humio endpoint to send the event to

    If token is missing, no notification is sent. If humio_url is not
    specified then the default, https://cloud.humio.com, will be used.

    """

    token = settings.get("token")
    isotimestamp = datetime.fromtimestamp(event["ts"], timezone.utc).isoformat()
    humio_url = settings.get("humio_url")

    if not token:
        logger.debug("Humio notifier requires a token")
        return

    if not humio_url:
        logger.info("Falling back to default Humio URL")
        humio_url = "https://cloud.humio.com"

    token = token.strip()
    url = "{}/api/v1/ingest/humio-structured".format(humio_url)

    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }

    host = platform.node()
    payload = [
        {
            "tags": {
                "host": host,
                "platform": platform.platform(),
                "python": platform.python_version(),
                "system": platform.system(),
                "machine": platform.machine(),
                "provider": "chaostoolkit",
                "chaosengineering": "true",
            },
            "events": [
                {"timestamp": isotimestamp, "attributes": event["payload"]},
            ],
        }
    ]

    r = requests.post(url, headers=headers, json=payload, timeout=(2, 10))
    if r.status_code > 399:
        logger.debug(
            "Failed to post to Humio with status code of {status} with"
            " reason: {reason}".format(status=r.status_code, reason=r.text)
        )
