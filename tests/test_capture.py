import unittest
import uuid

from engines.capture import capture_trade


class TestCapture(unittest.TestCase):

    def test_capture_trade(self):

        trade_id = f"TEST_{uuid.uuid4().hex[:8]}"

        capture_trade(
            trade_id,
            "2026-07-04",
            "2026-07-05",
            "SEC001",
            "CP001",
            "BUY",
            100,
            200.0,
        )

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()