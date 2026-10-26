"""Offline checks for safe coordinator error classification and log hygiene."""
from __future__ import annotations

import ast
from pathlib import Path
import unittest

PACKAGE = Path(__file__).resolve().parents[1] / "custom_components" / "jd_smart"


class SafeDiagnosticsTest(unittest.TestCase):
    def test_non_auth_snapshot_failures_do_not_request_reauthentication(self):
        source = (PACKAGE / "coordinator.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        coordinator = next(
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "JdSmartCoordinator"
        )
        handler = next(
            node for node in coordinator.body
            if isinstance(node, ast.AsyncFunctionDef)
            and node.name == "_async_handle_update_failure"
        )
        self.assertNotIn("ConfigEntryAuthFailed", ast.unparse(handler))
        self.assertIn("UpdateFailed", ast.unparse(handler))

    def test_periodic_snapshot_fetches_full_state(self):
        source = (PACKAGE / "coordinator.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        coordinator = next(
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "JdSmartCoordinator"
        )
        updater = next(
            node for node in coordinator.body
            if isinstance(node, ast.AsyncFunctionDef) and node.name == "_async_update_data"
        )
        body = ast.unparse(updater)
        self.assertIn("digest = ''", body)
        self.assertNotIn("self.data.digest if self.data", body)

    def test_http_failures_do_not_log_response_body(self):
        source = (PACKAGE / "api.py").read_text(encoding="utf-8")
        self.assertNotIn("_truncate(text)", source)
        self.assertNotIn("_truncate(json.dumps(payload", source)
        self.assertIn("body_length=%s", source)
        self.assertIn("JdSmartAuthError(\"JD Smart credentials rejected (HTTP 401)\")", source)


if __name__ == "__main__":
    unittest.main()
