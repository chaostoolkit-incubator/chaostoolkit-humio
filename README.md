# chaostoolkit-humio

[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-humio.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-humio)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-humio.svg)](https://www.python.org/)

This project is an extension for the Chaos Toolkit to target [Humio][humio].

[humio]: https://www.humio.com/

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install -U chaostoolkit-humio
```

## Humio Token

To use this extension, you will need one piece of information from Humio, the
[API token][token] for a user.

[token]: https://cloud.humio.com/docs/http-api/index.html#api-token

## Usage

This extension can be used a control on the experiment or a notification
plugin of the Chaos Toolkit CLI itself. Usually, only one of these two methods
is used at any given time as they serve similar purpose but feel free to
combine them. The control approach is deeper because it logs down to the
activity whereas notifications are much higher level.

### Notification

To use this extension to push notifications, edit your
[chaostoolkit settings][settings] by adding the following payload:

[settings]: https://docs.chaostoolkit.org/reference/usage/cli/#configure-the-chaos-toolkit

```yaml
notifications:
  -
    type: plugin
    module: chaoshumio.notification
    humio_url: https://myhumio.company.com
    token: my-token
```

By default all events will be forwarded to that channel. You may filter only
those events you care for:


```yaml
notifications:
  -
    type: plugin
    module: chaoshumio.notification
    humio_url: https://myhumio.company.com
    token: my-token
    events:
      - run-failed
      - run-started
```

Only sends those two events.

### Control

To use this extension as a control over the experiment and send logs during
the execution of the experiment to `https://cloud.humio.com`, add the following
payload to your experiment:

```json
{
    "secrets": {
        "humio": {
            "token": {
                "type": "env",
                "key": "HUMIO_INGEST_TOKEN"
            }
        }
    },
    "controls": [
        {
            "name": "humio-logger",
            "provider": {
                "type": "python",
                "module": "chaoshumio.control",
                "secrets": ["humio"]
            }
        }
    ]
}
```

If you want to send logs to a different Humio URL endpoint, specify the
`humio_url` configuration parameter. The following shows how this parameter:

```json
{
    "secrets": {
        "humio": {
            "token": {
                "type": "env",
                "key": "HUMIO_INGEST_TOKEN"
            }
        }
    },
    "configuration": {
        "humio_url": "https://myhumio.company.com"
    },
    "controls": [
        {
            "name": "humio-logger",
            "provider": {
                "type": "python",
                "module": "chaoshumio.control",
                "secrets": ["humio"]
            }
        }
    ]
}
```

This will ensure the results of the experiment, steady-state, method, rollbacks
and each activity are sent to Humio. The experiment itself will also be
send initially.

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
