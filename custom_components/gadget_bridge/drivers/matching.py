"""Deterministic, explicit BLE recognition independent of HA transport."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Advertisement:
    name: str
    service_uuids: frozenset[str]


@dataclass(frozen=True)
class MatchRule:
    driver_id: str
    services: frozenset[str]
    name_prefix: str | None = None

    def matches(self, advertisement: Advertisement) -> bool:
        if not self.services:
            return False
        advertised = {value.lower() for value in advertisement.service_uuids}
        return (
            {value.lower() for value in self.services} <= advertised
            and (self.name_prefix is None or advertisement.name.casefold().startswith(self.name_prefix.casefold()))
        )


def matching_drivers(advertisement: Advertisement, rules: tuple[MatchRule, ...]) -> tuple[str, ...]:
    """Return all matching driver IDs, without guessing among ambiguous matches."""
    return tuple(sorted({rule.driver_id for rule in rules if rule.matches(advertisement)}))


STANDARD_RULES = tuple(
    MatchRule("standard_gatt", frozenset({f"0000{uuid}-0000-1000-8000-00805f9b34fb"}))
    for uuid in ("180d", "180f", "181d")
)
