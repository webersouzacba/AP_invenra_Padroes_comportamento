from __future__ import annotations

from typing import Any, Dict

from .observer import DomainEvent, Observer
from .persistence_proxy import PersistenceProxy


class PersistenceEventObserver(Observer):
    """
    Observer concreto: persiste eventos usando o PersistenceProxy.append_event(...).
    """

    def __init__(self, proxy: PersistenceProxy) -> None:
        self._proxy = proxy

    def update(self, event: DomainEvent) -> None:
        payload: Dict[str, Any] = {
            "ts": event.occurred_at,
            "type": event.name,
            **event.payload,
        }
        self._proxy.append_event(payload)
