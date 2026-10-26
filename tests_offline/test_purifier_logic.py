"""Offline tests that never contact JD servers or control devices."""

import importlib.util
from pathlib import Path
import unittest


TARGET = Path(__file__).resolve().parents[1] / "custom_components" / "jd_smart" / "purifier_protocol.py"
spec = importlib.util.spec_from_file_location("jd_purifier_protocol", TARGET)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PurifierMappingTest(unittest.TestCase):
    def test_name_recognition(self):
        self.assertTrue(module.looks_like_purifier("京东京造灵犀 600G Pro"))
        self.assertTrue(module.looks_like_purifier("家电", "净水设备"))
        self.assertTrue(module.looks_like_purifier("Water Purifier"))
        self.assertFalse(module.looks_like_purifier("卧室空调"))

    def test_no_commands_without_capture(self):
        for opts in ({}, {"flush_stream_id": "wash"}, {"flush_value": "1"}):
            self.assertIsNone(module.resolve_flush_command(opts, "123", ["123"]))

    def test_explicit_mapping_exact_target(self):
        options = {"flush_feed_id": "200", "flush_stream_id": "rinsing", "flush_value": "1"}
        self.assertEqual(module.resolve_flush_command(options, "200", ["100", "200"]), {"rinsing": "1"})
        self.assertIsNone(module.resolve_flush_command(options, "100", ["100", "200"]))

    def test_ambiguity_disables_button(self):
        options = {"flush_stream_id": "wash", "flush_value": "1"}
        self.assertIsNone(module.resolve_flush_command(options, "100", ["100", "200"]))
        self.assertEqual(module.resolve_flush_command(options, "100", ["100"]), {"wash": "1"})

    def test_manto_readonly_sensor_semantics(self):
        labels = module.MANTO_STREAM_LABELS
        self.assertEqual(labels["PureTDS"], "纯水 TDS")
        self.assertEqual(labels["Wash"], "一键冲洗状态（原始值）")
        self.assertEqual(labels["Filter1Life"], "一级滤芯寿命")
        self.assertEqual(labels["Filter2Life"], "二级滤芯寿命")
        self.assertEqual(module.MANTO_STREAM_UNITS["PureTDS"], "ppm")
        self.assertEqual(module.MANTO_STREAM_UNITS["Filter1Life"], "%")
        self.assertEqual(module.MANTO_NUMERIC_STREAMS, frozenset({"PureTDS", "Filter1Life", "Filter2Life"}))
        self.assertIsNone(module.resolve_flush_command({}, "123", ["123"]))

    def test_not_a_purifier_and_oversized_values(self):
        options = {"flush_stream_id": "wash", "flush_value": "1"}
        self.assertIsNone(module.resolve_flush_command(options, "300", ["100"]))
        options["flush_value"] = "a" * 260
        self.assertIsNone(module.resolve_flush_command(options, "100", ["100"]))


if __name__ == "__main__":
    unittest.main()
