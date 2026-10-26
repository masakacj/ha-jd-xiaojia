"""Minimal capture-gated purifier mapping logic, independent of Home Assistant."""

from __future__ import annotations

from collections.abc import Mapping

PURIFIER_HINTS = ("净水", "纯水", "净饮", "water purifier", "600g")

# Confirmed in the JD Manto mini-program's offline app-service.js. These
# descriptive labels do not authorize a cloud control request.
MANTO_STREAM_LABELS = {
    "PureTDS": "纯水 TDS",
    "State": "工作状态（原始值）",
    "Wash": "一键冲洗状态（原始值）",
    "Filter1Life": "一级滤芯寿命",
    "Filter2Life": "二级滤芯寿命",
    "ResetFilter": "滤芯复位状态（原始值）",
    "Offline": "设备在线状态（原始值）",
}
MANTO_NUMERIC_STREAMS = frozenset({"PureTDS", "Filter1Life", "Filter2Life"})
MANTO_STREAM_UNITS = {"PureTDS": "ppm", "Filter1Life": "%", "Filter2Life": "%"}


def looks_like_purifier(name: str, category_name: str = "") -> bool:
    """Match only a strong textual device name/category, not a guessed numeric ID."""
    text = f"{category_name} {name}".casefold()
    return any(hint in text for hint in PURIFIER_HINTS)


def resolve_flush_command(
    options: Mapping[str, str],
    feed_id: str,
    purifier_feed_ids: list[str],
) -> dict[str, str] | None:
    """Return only the capture-confirmed command for an unambiguous purifier."""
    stream_id = str(options.get("flush_stream_id", "")).strip()
    value = str(options.get("flush_value", "")).strip()
    selected = str(options.get("flush_feed_id", "")).strip()

    if not stream_id or not value or len(stream_id) > 120 or len(value) > 250:
        return None
    if feed_id not in purifier_feed_ids:
        return None
    if selected:
        if feed_id != selected:
            return None
    elif len(purifier_feed_ids) != 1 or purifier_feed_ids[0] != feed_id:
        return None
    return {stream_id: value}
