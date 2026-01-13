from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Protocol


@dataclass(frozen=True)
class DomainEvent:
    """
    Evento de domínio publicado pelo Activity Provider.
    """
    name: str
    occurred_at: str
    payload: Dict[str, Any]

    @staticmethod
    def now(name: str, payload: Dict[str, Any]) -> "DomainEvent":
        return DomainEvent(
            name=name,
            occurred_at=datetime.now(timezone.utc).isoformat(),
            payload=payload,
        )


class Observer(Protocol):
    def update(self, event: DomainEvent) -> None:
        ...


class Subject:
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: DomainEvent) -> None:
        for obs in list(self._observers):
            obs.update(event)
