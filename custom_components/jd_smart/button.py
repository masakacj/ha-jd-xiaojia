"""One-shot buttons for verified JD Xiaojia purifier commands."""

from __future__ import annotations

import asyncio

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    CONF_FLUSH_FEED_ID,
    CONF_FLUSH_STREAM_ID,
    CONF_FLUSH_VALUE,
    DEVICE_TYPE_WATER_PURIFIER,
)
from .coordinator import JdSmartConfigEntry
from .entity import JdSmartEntity
from .purifier_protocol import resolve_flush_command


async def async_setup_entry(
    hass: HomeAssistant,
    entry: JdSmartConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Only expose a flush button after exact capture-confirmed mapping."""
    opts = entry.options
    stream_id = str(opts.get(CONF_FLUSH_STREAM_ID, "")).strip()
    value = str(opts.get(CONF_FLUSH_VALUE, "")).strip()
    if not stream_id or not value:
        return
    purifiers = [
        coord
        for coord in entry.runtime_data.coordinators.values()
        if coord.device_type == DEVICE_TYPE_WATER_PURIFIER
    ]
    ids = [coord.feed_id for coord in purifiers]
    entities = []
    for coordinator in purifiers:
        mapping = resolve_flush_command(opts, coordinator.feed_id, ids)
        if mapping:
            actual_stream_id, actual_value = next(iter(mapping.items()))
            entities.append(JdSmartFlushButton(coordinator, actual_stream_id, actual_value))
    async_add_entities(entities)


class JdSmartFlushButton(JdSmartEntity, ButtonEntity):
    """Execute the captured one-shot flushing command."""

    _attr_icon = "mdi:water-sync"
    _attr_name = "一键冲洗"

    def __init__(self, coordinator, stream_id: str, value: str) -> None:
        super().__init__(coordinator, "one_shot_flush")
        self._stream_id = stream_id
        self._value = value
        self._lock = asyncio.Lock()

    @property
    def available(self) -> bool:
        """Do not start a flush without a known-online device snapshot."""
        return super().available and self.coordinator.data is not None

    async def async_press(self) -> None:
        """Never issue overlapping commands from this button instance."""
        if self._lock.locked():
            return
        async with self._lock:
            await self.coordinator.async_control_streams(
                {self._stream_id: self._value}
            )
