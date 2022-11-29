# Connect-4-Bot
The game being played is variation of connect-4. Scoring is determined by the number of streaks of 3 or larger. Each streak is scored as its length squared. Whoever has the higher score once the board is completely full is the winner.

The agent uses the minimax algorithm to play a variation of connect-4 against other agents or humans. Implemented a heuristic called by a depth limit agent to be able to compete on larger game boards. The game can be played by inputting into your terminal:

'python connect383.py first_player second_player board_size'

example for playing against the non-heuristic minimax agent:

'python connect383.py mini human 4x4'

