# -*- coding: utf-8 -*-
import platform
import time
from datetime import datetime, timezone

import requests_mock

from chaoshumio import push_to_humio
from chaoshumio.control import configure_control, with_logging


def test_push_to_humio(humio_url: str):
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    context = {
        "k0": "v0"
    }
    event = {
        "ts": timestamp,
        "name": "an-event",
        "type": "experiment",
        "context": context
    }
    secrets = {
        "token": "1234"
    }
    configuration = {
        "humio_url": humio_url
    }

    configure_control(secrets)
    with requests_mock.mock() as m:
        m.post(
            "{}/api/v1/ingest/humio-structured".format(humio_url),
            status_code=200,
            json=[{
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": context
                    },
                ]
            }]
        )
        push_to_humio(event, secrets, configuration)

        assert m.called


def test_push_to_humio_default_url():
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    context = {
        "k0": "v0"
    }
    event = {
        "ts": timestamp,
        "name": "an-event",
        "type": "experiment",
        "context": context
    }
    secrets = {
        "token": "1234"
    }
    configuration = {}

    configure_control(secrets)
    with requests_mock.mock() as m:
        m.post(
            "https://cloud.humio.com/api/v1/ingest/humio-structured",
            status_code=200,
            json=[{
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": context
                    },
                ]
            }]
        )
        push_to_humio(event, secrets, configuration)

        assert m.called


def test_push_context_to_humio(humio_url: str):
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    node = platform.node()
    context = {
        "k0": "v0"
    }
    event = {
        "ts": timestamp,
        "name": "an-event",
        "type": "experiment",
        "context": context
    }
    secrets = {
        "humio": {
            "token": "1234"
        }
    }
    configuration = {
        "humio_url": humio_url
    }

    configure_control(secrets)
    assert with_logging.enabled is True
    with requests_mock.mock() as m:
        m.post(
            "{}/api/v1/ingest/humio-structured".format(humio_url),
            status_code=200,
            json=[{
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": context
                    },
                ]
            }]
        )
        push_to_humio(event, secrets["humio"], configuration)

        assert m.called
        payload = m.last_request.json()[0]
        assert "tags" in payload
        assert payload["tags"] == {
            "chaosengineering": "true",
            'host': node, 'level': 'an-event',
            "platform": platform.platform(),
            "python": platform.python_version(),
            "system": platform.system(),
            "machine": platform.machine(),
            'provider': 'chaostoolkit', 'type': 'experiment'
        }
        assert payload["events"][0]["attributes"] == context


def test_push_state_to_humio(humio_url: str):
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    node = platform.node()
    context = {
        "k0": "v0"
    }
    state = {
        "s0": "v0"
    }
    event = {
        "ts": timestamp,
        "name": "an-event",
        "type": "experiment",
        "context": context,
        "state": state
    }
    secrets = {
        "humio": {
            "token": "1234"
        }
    }
    configuration = {
        "humio_url": humio_url
    }

    configure_control(secrets)
    assert with_logging.enabled is True
    with requests_mock.mock() as m:
        m.post(
            "{}/api/v1/ingest/humio-structured".format(humio_url),
            status_code=200,
            json=[{
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": state
                    }
                ]
            }]
        )
        push_to_humio(event, secrets["humio"], configuration)

        assert m.called
        payload = m.last_request.json()[0]
        assert "tags" in payload
        assert payload["tags"] == {
            "chaosengineering": "true",
            'host': node, 'level': 'an-event',
            "platform": platform.platform(),
            "python": platform.python_version(),
            "system": platform.system(),
            "machine": platform.machine(),
            'provider': 'chaostoolkit', 'type': 'experiment'
        }
        assert payload["events"][0]["attributes"] == state


def test_logger_disabled_when_missing_token(humio_url: str):
    timestamp = time.time()
    isotimestamp = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()

    context = {
        "k0": "v0"
    }
    state = {
        "s0": "v0"
    }
    event = {
        "ts": timestamp,
        "name": "an-event",
        "type": "experiment",
        "context": context,
        "state": state
    }
    secrets = {
        "humio": {}
    }
    configuration = {
        "humio_url": humio_url
    }

    configure_control(secrets)
    assert with_logging.enabled is False
    with requests_mock.mock() as m:
        m.post(
            "{}/api/v1/ingest/humio-structured".format(humio_url),
            status_code=200,
            json=[{
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": state
                    },
                ]
            }]
        )
        push_to_humio(event, secrets["humio"], configuration)
        assert m.called is False
