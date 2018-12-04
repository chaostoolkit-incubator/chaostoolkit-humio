# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import platform
import time
import types
from unittest.mock import MagicMock, patch

from chaoslib.notification import RunFlowEvent
import pytest
import requests
import requests_mock

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
        "token": "1234",
        "dataspace": "default"
    }

    configure_control(None, secrets)
    assert with_logging.enabled is True
    with requests_mock.mock() as m:
        m.post(
            'https://cloud.humio.com/api/v1/dataspaces/default/ingest',
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
        push_to_humio(event, secrets)

        assert m.called
        payload = m.last_request.json()[0]
        assert "tags" in payload
        assert payload["tags"] == {
            'host': node, 'level': 'an-event',
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
        "token": "1234",
        "dataspace": "default"
    }

    configure_control(None, secrets)
    assert with_logging.enabled is True
    with requests_mock.mock() as m:
        m.post(
            'https://cloud.humio.com/api/v1/dataspaces/default/ingest',
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
        push_to_humio(event, secrets)

        assert m.called
        payload = m.last_request.json()[0]
        assert "tags" in payload
        assert payload["tags"] == {
            'host': node, 'level': 'an-event',
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
        "dataspace": "default"
    }

    configure_control(None, secrets)
    assert with_logging.enabled is False
    with requests_mock.mock() as m:
        m.post(
            'https://cloud.humio.com/api/v1/dataspaces/default/ingest',
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
        push_to_humio(event, secrets)
        assert m.called is False


def test_logger_disabled_when_missing_dataspace():
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
        "token": "123"
    }

    configure_control(None, secrets)
    assert with_logging.enabled is False
    with requests_mock.mock() as m:
        m.post(
            'https://cloud.humio.com/api/v1/dataspaces/default/ingest',
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
        push_to_humio(event, secrets)
        assert m.called is False
