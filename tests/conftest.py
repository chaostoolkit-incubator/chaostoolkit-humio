# -*- coding: utf-8 -*-
from typing import Any

import pytest

humio_domains = ["https://cloud.humio.com", "https://my.custom.com"]


@pytest.fixture(params=humio_domains)
def humio_url(request) -> Any:  # type: ignore
    return request.param
