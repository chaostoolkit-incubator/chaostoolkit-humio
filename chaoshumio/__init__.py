# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import os
import os.path
import platform
from typing import Any, Dict

from chaoslib.types import Configuration, EventPayload, Secrets
from logzero import logger
import requests

__all__ = ["__version__", "push_to_humio"]
__version__ = '0.3.0'


def push_to_humio(event: EventPayload, secrets: Secrets):
    """
    Send the event payload to Humio

    The `secrets` must contain `token` and `dataspace` properties. The former
    is the Humio token and the latter is the space where to push the event to.

    If any of those two properties are missing, the function logs a message
    and immediately returns.

    This function does not add any identifier to the payload, so make sure
    the even has one if you need correlation.
    """
    token = secrets.get("token", "").strip()
    if not token:
        logger.debug("Missing Humio token secret")
        return

    dataspace = secrets.get("dataspace", "").strip()
    if not dataspace:
        logger.debug("Missing Humio dataspace")
        return

    isotimestamp = datetime.fromtimestamp(
        datetime.utcnow().replace(tzinfo=timezone.utc).timestamp(),
        timezone.utc).isoformat()

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
            "level": event["name"],
            "chaosengineering": "true",
            "platform": platform.platform(),
            "python": platform.python_version(),
            "system": platform.system(),
            "machine": platform.machine(),
            "provider": "chaostoolkit",
            "type": event.get("type", "experiment")
        },
        "events": []
    }]

    if "state" in event:
        payload[0]["events"].append(
            {
                "timestamp": isotimestamp,
                "attributes": event["state"]
            }
        )
    else:
        payload[0]["events"].append(
            {
                "timestamp": isotimestamp,
                "attributes": event["context"]
            }
        )

    r = requests.post(url, headers=headers, json=payload, timeout=(2, 3))
    if r.status_code > 399:
        logger.debug(
            "Failed to post to Humio with status code of {status} with"
            " reason: {reason}".format(
                status=r.status_code, reason=r.text))
