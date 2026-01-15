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


class AnalyticsEventObserver(Observer):
    """
    Observer concreto: calcula métricas agregadas a partir de eventos e
    persiste apenas os agregados (não duplica o event log).

    Nesta atividade, agregamos a contagem de acessos ao jogo por activityID.
    """

    def __init__(self, proxy: PersistenceProxy) -> None:
        self._proxy = proxy

    def update(self, event: DomainEvent) -> None:
        # Exemplo de agregado: contagem de acessos ao jogo
        if event.name != "game_access":
            return
        activity_id = str(event.payload.get("activityID") or "")
        if not activity_id:
            return
        self._proxy.increment_aggregate(
            activity_id, "game_access_count", delta=1)
