# Context
In poker, there's a game called progressive nit game. There's a fixed amount of buttons at the start of each cycle, and you get a button if you win a hand. At the end, whoever doesn't have a button must pay a fixed amount per button to everyone without a button.

Example: 7 players, 10 buttons, $4/button

Situation 1: At the end, 1 player doesn't have a button. They must pay $4/button to everyone who have at least 1 button, so each button is worth $4.

Situation 2: At the end, 2 players don't have a button. They both must pay $4/button to everyone who have at least 1 button, so each button is worth $8.

Situation 3: You won all 10 buttons. The other 9 players must pay you $4/button, so you get $36/button, so you get $360.

Can you properly calculate how much each button should be worth for you as well as other players and adjust your strategy accordingly?

# Usage
Example:

Getting EV if you have 2 buttons, 3 buttons remaining and 4 players without button
```bash 
python3 script.py ev 2 3 4
```
Getting genie payment if you have 0 button, 1 button remaining and 4 players without button
```bash
python3 script.py genie 0 1 4
```
Getting both EV and genie matrix if there are 9 buttons remaining
```bash
python3 script.py matrix 9
```