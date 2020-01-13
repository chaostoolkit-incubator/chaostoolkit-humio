# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import platform

from chaoslib.types import Configuration, EventPayload, Secrets
from logzero import logger
import requests

__all__ = ["__version__", "push_to_humio"]
__version__ = '0.3.0'


def push_to_humio(event: EventPayload, secrets: Secrets,
                  configuration: Configuration = None):
    """
    Send the event payload to Humio

    The `secrets` must contain a `token` property. The former
    is the Humio token. If this property is missing then the function
    will log a message and immediatley return.

    Optionally the `configuration` can contain a `humio_url` entry. This will
    override the default domain of your Humio service. The default is
    https://cloud.humio.com.

    This function does not add any identifier to the payload, so make sure
    the event has one if you need correlation.
    """
    token = secrets.get("token", "").strip()
    if not token:
        logger.debug("Missing Humio token secret")
        return

    humio_url = "https://cloud.humio.com"
    if configuration:
        configured_humio_url = configuration.get("humio_url", "").strip()
        if configured_humio_url:
            humio_url = configured_humio_url

    isotimestamp = datetime.fromtimestamp(
        datetime.utcnow().replace(tzinfo=timezone.utc).timestamp(),
        timezone.utc).isoformat()

    token = token.strip()
    url = "{}/api/v1/ingest/humio-ingest".format(
        humio_url)

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
