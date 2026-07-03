from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "instagram-account" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from fetch_metrics import compact_metrics, content_item_from_media, is_reel, observation


class InstagramFetchMetricsTest(unittest.TestCase):
    def test_reel_detection_uses_media_product_type(self) -> None:
        self.assertTrue(is_reel({"media_type": "VIDEO", "media_product_type": "REELS"}))
        self.assertTrue(is_reel({"media_type": "REELS"}))
        self.assertFalse(is_reel({"media_type": "VIDEO", "media_product_type": "FEED"}))

    def test_compact_metrics_preserves_watch_time_items_for_ui_projection(self) -> None:
        content = content_item_from_media(
            {
                "id": "18000850874933138",
                "media_type": "VIDEO",
                "media_product_type": "REELS",
                "permalink": "https://www.instagram.com/reel/DZHiKs4RMeu/",
            }
        )
        content["content_metrics"]["avg_watch_time"] = 4467.0
        content["content_metrics"]["total_watch_time"] = 491402.0

        metrics = compact_metrics(
            [
                observation("instagram_avg_watch_time", 4467.0, "2026-07-02"),
                observation("instagram_total_watch_time", 491402.0, "2026-07-02"),
            ],
            [content],
        )

        avg_item = metrics["instagram_avg_watch_time"]["items"][0]
        total_item = metrics["instagram_total_watch_time"]["items"][0]
        self.assertEqual(avg_item["kind"], "reels")
        self.assertEqual(avg_item["media_type"], "VIDEO")
        self.assertEqual(avg_item["media_product_type"], "REELS")
        self.assertEqual(avg_item["value"], 4467.0)
        self.assertEqual(total_item["value"], 491402.0)


if __name__ == "__main__":
    unittest.main()
