import sys
from pathlib import Path

# Add parent directory to path so we can import script
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from script import (
    expected_value_recurrence,
    closed_form_ev,
    TOTAL_PLAYERS,
    TOTAL_BUTTONS,
)


class TestExpectedValueFormulas(unittest.TestCase):
    """Test that recurrence and closed form EV formulas produce similar results."""

    def test_recurrence_vs_closed_form_within_tolerance(self):
        """Verify recurrence EV and closed form EV are close to each other."""
        tolerance = 1e-6
        failures = []

        for buttons_remaining in range(TOTAL_BUTTONS + 1):
            buttons_given_out = TOTAL_BUTTONS - buttons_remaining
            pwb_min = max(0, TOTAL_PLAYERS - buttons_given_out - 1)
            pwb_max = TOTAL_PLAYERS - 1

            for buttons_owned in range(TOTAL_BUTTONS + 1 - buttons_remaining):
                for players_without_button in range(pwb_min, pwb_max + 1):
                    recurrence_ev = expected_value_recurrence(
                        buttons_owned, buttons_remaining, players_without_button
                    )
                    closed_ev = closed_form_ev(
                        buttons_owned, buttons_remaining, players_without_button
                    )
                    diff = abs(recurrence_ev - closed_ev)

                    if diff > tolerance:
                        failures.append(
                            f"buttons_owned={buttons_owned}, "
                            f"buttons_remaining={buttons_remaining}, "
                            f"players_without_button={players_without_button}: "
                            f"recurrence={recurrence_ev:.4f}, "
                            f"closed_form={closed_ev:.4f}, "
                            f"diff={diff:.4f}"
                        )

        if failures:
            self.fail(
                f"Found {len(failures)} case(s) where difference exceeds {tolerance}:\n"
                + "\n".join(failures[:10])  # Show first 10 failures
                + (f"\n... and {len(failures) - 10} more" if len(failures) > 10 else "")
            )


if __name__ == "__main__":
    unittest.main()

