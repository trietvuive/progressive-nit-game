from functools import lru_cache

TOTAL_PLAYERS = 7
TOTAL_BUTTONS = 10
BUTTON_VALUE = 4

"""
Expected value of the progressive nit game
    buttons_owned: number of buttons that you have
    buttons_remaining: number of buttons remaining
    players_without_button: number of other players without a button (excluding yourself)
    it doesn't matter how the rest of the buttons you don't have are distributed
"""


@lru_cache(maxsize=None)
def expected_value_recurrence(
    buttons_owned: float, buttons_remaining: float, players_without_button: float
) -> float:
    # when the game resolves, you get -40 if you have no button
    # otherwise, you get BUTTON_VALUE * players_without_button for each button you own
    if buttons_remaining == 0:
        return (
            -BUTTON_VALUE * TOTAL_BUTTONS
            if buttons_owned == 0
            else buttons_owned * BUTTON_VALUE * players_without_button
        )

    # you win a button with probability 1 / TOTAL_PLAYERS
    ev_you_win_button = (
        1
        / TOTAL_PLAYERS
        * expected_value_recurrence(
            buttons_owned + 1, buttons_remaining - 1, players_without_button
        )
    )
    # people who don't have buttons win a button with probability players_without_button / TOTAL_PLAYERS
    ev_losers_win_button = (
        players_without_button
        / TOTAL_PLAYERS
        * expected_value_recurrence(
            buttons_owned, buttons_remaining - 1, players_without_button - 1
        )
    )
    # people who have buttons win a button with probability (TOTAL_PLAYERS - 1 - players_without_button) / TOTAL_PLAYERS
    ev_winners_win_button = (
        (TOTAL_PLAYERS - 1 - players_without_button)
        / TOTAL_PLAYERS
        * expected_value_recurrence(
            buttons_owned, buttons_remaining - 1, players_without_button
        )
    )

    return ev_you_win_button + ev_losers_win_button + ev_winners_win_button


"""
Closed form expected value formula
"""


def closed_form_ev(buttons_owned, buttons_remaining, players_without_button):
    # Probability a specific player misses a specific button
    q = (TOTAL_PLAYERS - 1) / TOTAL_PLAYERS

    # Probability a loser loses ALL remaining r buttons
    prob_lose_all = q**buttons_remaining

    # Probability a loser loses r-1 buttons
    # (Used when you 'consume' one button by winning it yourself)
    prob_lose_others = q ** (buttons_remaining - 1)

    if buttons_owned > 0:
        # Path 1: Value from buttons you currently hold
        # These buttons only pay out if the 'm' losers lose ALL remaining r buttons
        holdings_ev = buttons_owned * players_without_button * prob_lose_all

        # Path 2: Value from buttons you are expected to win (r/TOTAL_PLAYERS)
        # For each button you win, the 'm' losers only need to lose the OTHER r-1 buttons
        expected_new_buttons = buttons_remaining / TOTAL_PLAYERS
        gains_ev = expected_new_buttons * players_without_button * prob_lose_others

        return BUTTON_VALUE * (holdings_ev + gains_ev)

    else:
        # If you own 0, you have two mutually exclusive futures:

        # Future A: You win at least one button (Expected Reward)
        # Same logic as 'gains_ev' above
        expected_new_buttons = buttons_remaining / TOTAL_PLAYERS
        reward_ev = expected_new_buttons * players_without_button * prob_lose_others

        # Future B: You win ZERO buttons (Expected Penalty)
        # Probability of winning zero is q^r
        penalty_ev = TOTAL_BUTTONS * prob_lose_all

        return BUTTON_VALUE * (reward_ev - penalty_ev)


"""
The maximum amount you should pay genie to win a button is the expected value of winning a button minus your current expected value
    buttons_owned: number of buttons that you have
    buttons_remaining: number of buttons remaining
    players_without_button: number of other players without a button (excluding yourself)
"""


def calculate_genie_amount(
    buttons_owned: float, buttons_remaining: float, players_without_button: float
) -> float:
    return expected_value_recurrence(
        buttons_owned + 1, buttons_remaining - 1, players_without_button
    ) - expected_value_recurrence(
        buttons_owned, buttons_remaining, players_without_button
    )


def print_matrix(buttons_remaining: int):
    """Print 2D matrices of EV and genie values for a given number of buttons remaining."""
    # Calculate valid range for players_without_button: min is TOTAL_PLAYERS - (# buttons given out) - 1
    buttons_given_out = TOTAL_BUTTONS - buttons_remaining
    pwb_min = max(0, TOTAL_PLAYERS - buttons_given_out - 1)
    pwb_max = TOTAL_PLAYERS - 1

    # Header row
    header = "own\\pwb |" + "".join(f"{pwb:>8}" for pwb in range(pwb_min, pwb_max + 1))
    separator = "-" * len(header)

    # EV Matrix
    print(f"\n=== EV Matrix for buttons_remaining={buttons_remaining} ===")
    print(f"Rows: buttons_owned, Columns: players_without_button\n")
    print(header)
    print(separator)

    for buttons_owned in range(TOTAL_BUTTONS + 1 - buttons_remaining):
        row = f"{buttons_owned:>7} |"
        for pwb in range(pwb_min, pwb_max + 1):
            ev = expected_value_recurrence(buttons_owned, buttons_remaining, pwb)
            row += f"{ev:>8.2f}"
        print(row)

    # Genie Matrix (only if buttons_remaining > 0)
    if buttons_remaining > 0:
        print(f"\n=== Genie Matrix for buttons_remaining={buttons_remaining} ===")
        print(f"Rows: buttons_owned, Columns: players_without_button\n")
        print(header)
        print(separator)

        for buttons_owned in range(TOTAL_BUTTONS + 1 - buttons_remaining):
            row = f"{buttons_owned:>7} |"
            for pwb in range(pwb_min, pwb_max + 1):
                genie = calculate_genie_amount(buttons_owned, buttons_remaining, pwb)
                row += f"{genie:>8.2f}"
            print(row)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Progressive Nit Game Calculator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command 1: ev
    ev_parser = subparsers.add_parser("ev", help="Calculate expected value")
    ev_parser.add_argument("buttons_owned", type=int, help="Number of buttons you have")
    ev_parser.add_argument(
        "buttons_remaining", type=int, help="Number of buttons remaining"
    )
    ev_parser.add_argument(
        "players_without_button",
        type=int,
        help="Number of other players without a button",
    )

    # Command 2: genie
    genie_parser = subparsers.add_parser(
        "genie", help="Calculate max amount to pay genie"
    )
    genie_parser.add_argument(
        "buttons_owned", type=int, help="Number of buttons you have"
    )
    genie_parser.add_argument(
        "buttons_remaining", type=int, help="Number of buttons remaining"
    )
    genie_parser.add_argument(
        "players_without_button",
        type=int,
        help="Number of other players without a button",
    )

    # Command 3: matrix
    matrix_parser = subparsers.add_parser(
        "matrix", help="Print 2D matrix for given buttons remaining"
    )
    matrix_parser.add_argument(
        "buttons_remaining", type=int, help="Number of buttons remaining"
    )

    args = parser.parse_args()

    if args.command == "ev":
        ev = closed_form_ev(
            args.buttons_owned, args.buttons_remaining, args.players_without_button
        )
        print(
            f"EV(buttons_owned={args.buttons_owned}, buttons_remaining={args.buttons_remaining}, players_without_button={args.players_without_button}) = {ev:.2f}"
        )
    elif args.command == "genie":
        amount = calculate_genie_amount(
            args.buttons_owned, args.buttons_remaining, args.players_without_button
        )
        print(
            f"Max genie payment(buttons_owned={args.buttons_owned}, buttons_remaining={args.buttons_remaining}, players_without_button={args.players_without_button}) = {amount:.2f}"
        )
    elif args.command == "matrix":
        print_matrix(args.buttons_remaining)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
