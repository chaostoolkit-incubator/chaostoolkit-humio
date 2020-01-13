# -*- coding: utf-8 -*-
import time
import types
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
import requests
import requests_mock
from chaoslib.notification import RunFlowEvent

from chaoshumio.notification import notify


def test_notify():
    payload = {
        "msg": "hello"
    }
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    event_payload = {
        "ts": timestamp,
        "event": str(RunFlowEvent.RunStarted),
        "phase": "run",
        "payload": payload
    }
    with requests_mock.mock() as m:
        m.post(
            'https://cloud.humio.com/api/v1/ingest/humio-ingest',
            status_code=200,
            json=[ { 
                "tags": {
                    "host": "fake-host"
                },
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": payload
                    },
                ]
            } ]
        )

        notify(
            {
                "token": "my-token"
            },
            event_payload
        )

        assert m.called


def test_notify_custom_URL():
    payload = {
        "msg": "hello"
    }
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    event_payload = {
        "ts": timestamp,
        "event": str(RunFlowEvent.RunStarted),
        "phase": "run",
        "payload": payload
    }

    humio_url = "https://myhumio.company.com"

    with requests_mock.mock() as m:
        m.post(
            "{}/api/v1/ingest/humio-ingest".format(humio_url),
            status_code=200,
            json=[ { 
                "tags": {
                    "host": "fake-host"
                },
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": payload
                    },
                ]
            } ]
        )

        notify(
            {
                "token": "my-token",
                "humio_url": humio_url
            },
            event_payload
        )

        assert m.called
