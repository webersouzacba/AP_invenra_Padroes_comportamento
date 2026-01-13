from __future__ import annotations

from .observer import DomainEvent, Subject


class EventBus(Subject):
    """
    Subject concreto: publica eventos do Activity Provider.
    """

    def publish(self, event: DomainEvent) -> None:
        self.notify(event)
