# -*- coding: utf-8 -*-
import time
from datetime import datetime, timezone

import requests_mock
from chaoslib.notification import RunFlowEvent

from chaoshumio.notification import notify


def test_notify(humio_url: str) -> None:
    payload = {"msg": "hello"}
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    event_payload = {
        "ts": timestamp,
        "event": str(RunFlowEvent.RunStarted),
        "phase": "run",
        "payload": payload,
    }
    with requests_mock.mock() as m:
        m.post(
            "{}/api/v1/ingest/humio-structured".format(humio_url),
            status_code=200,
            json=[
                {
                    "tags": {"host": "fake-host"},
                    "events": [
                        {"timestamp": isotimestamp, "attributes": payload},
                    ],
                }
            ],
        )

        notify({"token": "my-token", "humio_url": humio_url}, event_payload)

        assert m.called


def test_notify_default_url() -> None:
    payload = {"msg": "hello"}
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    event_payload = {
        "ts": timestamp,
        "event": str(RunFlowEvent.RunStarted),
        "phase": "run",
        "payload": payload,
    }
    with requests_mock.mock() as m:
        m.post(
            "https://cloud.humio.com/api/v1/ingest/humio-structured",
            status_code=200,
            json=[
                {
                    "tags": {"host": "fake-host"},
                    "events": [
                        {"timestamp": isotimestamp, "attributes": payload},
                    ],
                }
            ],
        )

        notify(
            {
                "token": "my-token",
            },
            event_payload,
        )

        assert m.called
