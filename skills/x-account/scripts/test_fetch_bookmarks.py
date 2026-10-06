from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).with_name("fetch_bookmarks.py")
if str(SCRIPT.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("fetch_bookmarks", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FetchBookmarksTests(unittest.TestCase):
    def test_paginates_and_preserves_unknown_saved_time(self) -> None:
        requests: list[tuple[str, dict[str, str]]] = []
        pages = iter([
            {"data": [{"id": "1", "author_id": "a", "text": "first", "created_at": "2026-09-20T00:00:00Z"}], "includes": {"users": [{"id": "a", "username": "one"}]}, "meta": {"next_token": "next"}},
            {"data": [{"id": "2", "author_id": "b", "text": "second"}], "includes": {"users": [{"id": "b", "username": "two"}]}, "meta": {}},
        ])
        with (
            patch.object(MODULE, "load_runtime_values", return_value={"FARPLANE_X_OAUTH2_ACCESS_TOKEN": "secret"}),
            patch.object(MODULE, "resolve_user", return_value=("u", {"data": {"username": "owner"}}, ["/2/users/:id"])),
            patch.object(MODULE, "api_get", side_effect=lambda path, _auth, params: (requests.append((path, params)), next(pages))[1]),
        ):
            payload = MODULE.fetch_bookmarks(max_pages=3)
        self.assertEqual([item["canonical_key"] for item in payload["items"]], ["x:1", "x:2"])
        self.assertTrue(all(item["bookmark_saved_at"] is None for item in payload["items"]))
        self.assertEqual(payload["coverage"]["status"], "complete")
        self.assertNotIn("secret", str(payload))
        self.assertEqual(requests[0][0], "/users/u/bookmarks")
        self.assertIn("tweet.fields", requests[0][1])
        self.assertNotIn("post.fields", requests[0][1])
        self.assertEqual(requests[1][1]["pagination_token"], "next")

    def test_expired_access_token_refreshes_once_and_retries(self) -> None:
        from urllib.error import HTTPError

        auths: list[str] = []

        def resolve(_values, auth):
            auths.append(auth)
            if len(auths) == 1:
                raise HTTPError("https://api.x.com/2/users/me", 401, "Unauthorized", {}, None)
            return "u", {"data": {"username": "owner"}}, ["/2/users/:id"]

        with (
            patch.object(MODULE, "load_runtime_values", return_value={"FARPLANE_X_OAUTH2_ACCESS_TOKEN": "stale"}),
            patch.object(MODULE, "refresh_oauth2_access_token", return_value="fresh") as refresh,
            patch.object(MODULE, "resolve_user", side_effect=resolve),
            patch.object(MODULE, "api_get", return_value={"data": [], "meta": {}}),
        ):
            payload = MODULE.fetch_bookmarks(max_pages=1)
        refresh.assert_called_once()
        self.assertEqual(auths, ["Bearer stale", "Bearer fresh"])
        self.assertEqual(payload["coverage"]["status"], "empty")

    def test_rotated_refresh_pair_is_private_and_wins_over_injected_values(self) -> None:
        import io
        import json
        import os
        import tempfile

        import runtime_env

        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {
            "FARPLANE_STATE_DIR": home,
            "FARPLANE_X_OAUTH2_ACCESS_TOKEN": "injected-access",
            "FARPLANE_X_OAUTH2_REFRESH_TOKEN": "injected-refresh",
            "FARPLANE_X_OAUTH2_CLIENT_ID": "client",
        }, clear=True):
            response = io.BytesIO(json.dumps({"access_token": "new-access", "refresh_token": "new-refresh"}).encode())
            with patch.object(runtime_env, "urlopen", return_value=response):
                values = runtime_env.load_runtime_values()
                self.assertEqual(runtime_env.refresh_oauth2_access_token(values), "new-access")
            state = runtime_env.oauth2_state_path()
            self.assertEqual(state.stat().st_mode & 0o777, 0o600)
            reloaded = runtime_env.load_runtime_values()
        self.assertEqual(reloaded["FARPLANE_X_OAUTH2_ACCESS_TOKEN"], "new-access")
        self.assertEqual(reloaded["FARPLANE_X_OAUTH2_REFRESH_TOKEN"], "new-refresh")

    def test_requires_user_oauth2(self) -> None:
        with patch.object(MODULE, "load_runtime_values", return_value={}):
            with self.assertRaisesRegex(RuntimeError, "OAUTH2_ACCESS_TOKEN"):
                MODULE.fetch_bookmarks()


if __name__ == "__main__":
    unittest.main()
