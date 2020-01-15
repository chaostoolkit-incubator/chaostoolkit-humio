# -*- coding: utf-8 -*-

import pytest


humio_domains = ["https://cloud.humio.com", "https://my.custom.com"]
@pytest.fixture(params=humio_domains)
def humio_url(request):
    return request.param
