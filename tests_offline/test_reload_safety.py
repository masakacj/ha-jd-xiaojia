"""Regression tests for JD Smart config entry update/reload flow."""
import ast
from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[1] / "custom_components" / "jd_smart"


def function_body(path: str, name: str) -> str:
    tree = ast.parse((BASE / path).read_text(encoding="utf8"))
    functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    assert len(functions) == 1, (path, name, len(functions))
    return ast.unparse(functions[0])


class ConfigEntryReloadSafetyTest(unittest.TestCase):
    def test_listener_uses_home_assistant_reload(self):
        body = function_body("__init__.py", "async_reload_entry")
        self.assertIn("hass.config_entries.async_reload(entry.entry_id)", body)
        self.assertNotIn("async_unload_entry(hass, entry)", body)
        self.assertNotIn("async_setup_entry(hass, entry)", body)

    def test_token_renewal_does_not_reload(self):
        body = function_body("__init__.py", "async_reload_entry")
        self.assertIn("runtime.client.credentials.cookie", body)
        self.assertIn("runtime.client.credentials.tgt", body)
        self.assertIn("runtime.configured_data", body)
        self.assertIn("runtime.configured_options", body)

    def test_manual_auth_has_no_second_reload(self):
        body = function_body("config_flow.py", "_async_update_auth_entries")
        self.assertIn("async_update_entry(entry, data=data)", body)
        self.assertNotIn("async_reload", body)

    def test_config_changes_snapshot_before_listener(self):
        body = function_body("__init__.py", "async_setup_entry")
        self.assertIn("configured_data=_data_without_tokens(entry.data)", body)
        self.assertIn("configured_options=deepcopy(entry.options)", body)


if __name__ == "__main__":
    unittest.main()
