# -*- coding: utf-8 -*-
import platform
import time
import types
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
import requests
import requests_mock
from chaoslib.notification import RunFlowEvent

from chaoshumio import push_to_humio
from chaoshumio.control import configure_control, with_logging


def test_push_context_to_humio():
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

    configure_control(None, secrets)
    assert with_logging.enabled is True
    with requests_mock.mock() as m:
        m.post(
            "https://cloud.humio.com/api/v1/ingest/humio-structured",
            status_code=200,
            json=[ {
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": context
                    },
                ]
            } ]
        )
        push_to_humio(event, secrets["humio"])

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


def test_push_context_to_humio_no_dataspace():
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

    configure_control(None, secrets)
    assert with_logging.enabled is True
    with requests_mock.mock() as m:
        m.post(
            "https://cloud.humio.com/api/v1/ingest/humio-structured",
            status_code=200,
            json=[ {
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": context
                    },
                ]
            } ]
        )
        push_to_humio(event, secrets["humio"])

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


def test_push_context_to_humio_custom_domain():
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
    humio_test_url = "https://my.humio.com"
    configuration = {
        "humio_url": humio_test_url
    }

    configure_control(None, secrets)
    assert with_logging.enabled is True
    with requests_mock.mock() as m:
        m.post(
            "{}/api/v1/ingest/humio-structured".format(humio_test_url),
            status_code=200,
            json=[ {
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": context
                    },
                ]
            } ]
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


def test_push_state_to_humio():
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
    configure_control(None, secrets)
    assert with_logging.enabled is True
    with requests_mock.mock() as m:
        m.post(
            'https://cloud.humio.com/api/v1/ingest/humio-structured',
            status_code=200,
            json=[ {
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": state
                    }
                ]
            } ]
        )
        push_to_humio(event, secrets["humio"])

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


def test_logger_disabled_when_missing_token():
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
        "humio": {}
    }

    configure_control(None, secrets)
    assert with_logging.enabled is False
    with requests_mock.mock() as m:
        m.post(
            'https://cloud.humio.com/api/v1/ingest/humio-structured',
            status_code=200,
            json=[ {
                "events": [
                    {
                        "timestamp": isotimestamp,
                        "attributes": state
                    },
                ]
            } ]
        )
        push_to_humio(event, secrets["humio"])
        assert m.called is False
