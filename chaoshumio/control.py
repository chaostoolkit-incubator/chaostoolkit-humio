# -*- coding: utf-8 -*-
import threading
from typing import Any, Dict, List

from chaoslib.types import Activity, Configuration, Experiment, Hypothesis, \
    Journal, Run, Secrets
from logzero import logger

from . import push_to_humio

__all__ = ["configure_control", "before_experiment_control",
           "after_experiment_control", "after_hypothesis_control",
           "after_method_control", "after_rollback_control",
           "after_activity_control"]

with_logging = threading.local()


def configure_control(configuration: Configuration, secrets: Secrets):
    """
    Enable logging to Humio if the `token` and `dataspace` are set in the
    `secrets` payload.
    """
    token = secrets.get("humio", {}).get("token", "").strip()
    if not token:
        logger.debug("Missing Humio token secret")
        with_logging.enabled = False
        return

    dataspace = secrets.get("humio", {}).get("dataspace", "").strip()
    if not dataspace:
        logger.debug("Missing Humio dataspace")
        with_logging.enabled = False
        return

    logger.debug("Humio logging control is active for this session")
    with_logging.enabled = True


def before_experiment_control(context: Experiment, secrets: Secrets):
    """
    Send the experiment
    """
    if not with_logging.enabled:
        return

    event = {
        "name": "before-experiment",
        "context": context,
    }
    push_to_humio(event=event, secrets=secrets)


def after_experiment_control(context: Experiment, state: Journal,
                             secrets: Secrets):
    """
    Send the experiment's journal
    """
    if not with_logging.enabled:
        return

    event = {
        "name": "after-experiment",
        "context": context,
        "state": state
    }
    push_to_humio(event=event, secrets=secrets)


def after_hypothesis_control(context: Hypothesis, state: Dict[str, Any],
                             secrets: Secrets):
    """
    Send the steady-state hypothesis's result
    """
    if not with_logging.enabled:
        return

    event = {
        "name": "after-hypothesis",
        "context": context,
        "state": state,
        "type": "hypothesis"
    }
    push_to_humio(event=event, secrets=secrets)


def after_method_control(context: Experiment, state: List[Run],
                         secrets: Secrets):
    """
    Send the method's result
    """
    if not with_logging.enabled:
        return

    event = {
        "name": "after-method",
        "context": context,
        "state": state,
        "type": "method"
    }
    push_to_humio(event=event, secrets=secrets)


def after_rollback_control(context: Experiment, state: List[Run],
                           secrets: Secrets):
    """
    Send the rollback's result
    """
    if not with_logging.enabled:
        return

    event = {
        "name": "after-rollback",
        "context": context,
        "state": state,
        "type": "rollback"
    }
    push_to_humio(event=event, secrets=secrets)


def after_activity_control(context: Activity, state: Run,
                           secrets: Secrets):
    """
    Send each activity's result
    """
    if not with_logging.enabled:
        return

    event = {
        "name": "after-activity",
        "context": context,
        "state": state,
        "type": "activity"
    }
    push_to_humio(event=event, secrets=secrets)
