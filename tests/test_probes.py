# -*- coding: utf-8 -*-
import platform
import time
from datetime import datetime, timezone

import requests_mock

from chaoshumio.probes import search_query


def test_search_query_probe(humio_url: str):
    with requests_mock.mock() as m:
        m.post(
            "{}/api/v1/repositories/sandbox/query".format(humio_url),
            json=[{"_count": 5}],
            headers={
                "content-type": "application/json"
            }
        )
        
        result = search_query(
            "app=hello", configuration={
                "humio_url": humio_url
            },
            secrets={"token": "123"})
        assert result == [{"_count": 5}]
