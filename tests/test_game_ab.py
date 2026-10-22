import unittest

import pandas as pd

from game_ab.analyze import analyze


class GameABTests(unittest.TestCase):
    def test_retention_uses_assigned_players_even_with_extreme_rounds(self):
        frame = pd.DataFrame(
            [
                (1, "gate_30", 1, True, True),
                (2, "gate_30", 50000, False, False),
                (3, "gate_30", 4, True, False),
                (4, "gate_30", 0, False, False),
                (5, "gate_40", 2, True, False),
                (6, "gate_40", 3, False, False),
                (7, "gate_40", 4, False, False),
                (8, "gate_40", 5, False, False),
            ], columns=["userid", "version", "sum_gamerounds", "retention_1", "retention_7"]
        )
        result = analyze(frame)
        self.assertEqual(result["players"], 8)
        self.assertEqual(result["groups"]["gate_30"]["d7_retained"], 1)
        self.assertEqual(result["groups"]["gate_40"]["d7_retained"], 0)
        self.assertAlmostEqual(result["effects"]["d1"]["rate_difference_pp"], -25.0)
        self.assertEqual(result["rounds_outliers_over_10000"], 1)
        self.assertAlmostEqual(result["srm"]["p_value"], 1.0)

    def test_duplicate_user_and_invalid_group_are_rejected(self):
        frame = pd.DataFrame([(1, "gate_30", 1, True, True), (1, "gate_40", 2, True, False)],
                             columns=["userid", "version", "sum_gamerounds", "retention_1", "retention_7"])
        with self.assertRaises(ValueError):
            analyze(frame)
        frame.loc[1, "userid"] = 2
        frame.loc[1, "version"] = "unknown"
        with self.assertRaises(ValueError):
            analyze(frame)


if __name__ == "__main__":
    unittest.main()
