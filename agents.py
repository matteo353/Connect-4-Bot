import random
import math


BOT_NAME = 'Matteo Jr'

class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
  
    rseed = None  # change this to a value if you want consistent random choices

    def __init__(self):
        if self.rseed is None:
            self.rstate = None
        else:
            random.seed(self.rseed)
            self.rstate = random.getstate()

    def get_move(self, state):
        if self.rstate is not None:
            random.setstate(self.rstate)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move.  Very slow and not always smart."""

    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Gets called by get_move() to determine the value of each successor state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state

        """
        if state.is_full():  # if we have reached the last possible state in the current path
            return state.utility()  # return the utility of that value

        elif state.next_player() == -1:  # the next player is minimum
            max_val = -math.inf  # initialize the max value to negative infinity
            successors = state.successors()

            for succ in successors:
                temp = self.minimax(succ[1])
                max_val = max(max_val, temp)
            return max_val

        elif state.next_player() == 1:
            min_val = math.inf
            successors = state.successors()

            for succ in successors:
                temp = self.minimax(succ[1])
                min_val = min(min_val, temp)
            return min_val

        print('error: did not reach final state')


class MinimaxLookaheadAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move.
 
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        Gets called by get_move() to determine the value of successor states.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the (possibly estimated) minimax utility value of the state
        """
        # at this point we have minimax that stops at a limit but need to implement what value is going to get returned
        def minimax_look(state, depth_lim):

            if depth_lim <= 0:  # change this
                # return self.evaluation(state)  # this is where you implement your heuristic
                return self.evaluation(state)

            elif state.next_player() == -1:

                max_val = -math.inf  # initialize the max value to negative infinity
                successors = state.successors()

                for succ in successors:
                    temp = minimax_look(succ[1], depth_lim-1)
                    max_val = max(max_val, temp)
                return max_val

            elif state.next_player() == 1:

                min_val = math.inf
                successors = state.successors()

                for succ in successors:
                    temp = minimax_look(succ[1], depth_lim-1)
                    min_val = min(min_val, temp)
                return min_val

        return minimax_look(state, self.depth_limit)

    def minimax_depth(self, state, depth):
        """This is just a helper method for minimax(). Feel free to use it or not. """
        pass

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        Gets called by minimax() once the depth limit has been reached.  
        N.B.: This method must run in "constant" time for all states!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heuristic estimate of the utility value of the state
        """
        rows = state.get_rows()
        columns = state.get_cols()
        diags = state.get_diags()
        full = rows + columns + diags
        player1 = 0
        player2 = 0
        for run in full:
            for elt, length in streaks(run):
                if elt == 1:  # player 1 piece
                    if length >= 2:
                        player1 += ((length + 1) ** 2) / 2
                elif elt == -1:
                    if length >= 2:
                        player2 += ((length + 1) ** 2) / 2
        return player1 - player2


class AltMinimaxLookaheadAgent(MinimaxAgent):
    """Alternative heursitic agent used for testing."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state."""

        return 19  # Change this line, unless you have something better to do.


class MinimaxPruneAgent(MinimaxAgent):
    """Computer agent that uses minimax with alpha-beta pruning to select the best move.
    
    Hint: Consider what you did for MinimaxAgent.  What do you need to change to prune a
    branch of the state space? 
    """
    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent does not have a depth limit.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to column 1 (we're trading optimality for gradeability here).

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        def minimax_prune(state, alpha, beta):

            if state.is_full():  # if we have reached the last possible state in the current path
                return state.utility()

            elif state.next_player() == -1:

                max_val = -math.inf  # initialize the max value to negative infinity
                successors = state.successors()

                for succ in successors:
                    temp = minimax_prune(succ[1], alpha, beta)
                    max_val = max(max_val, temp)
                    alpha = max(alpha, temp)
                    if beta <= alpha:
                        break
                return max_val

            elif state.next_player() == 1:

                min_val = math.inf
                successors = state.successors()

                for succ in successors:
                    temp = minimax_prune(succ[1], alpha, beta)
                    min_val = min(min_val, temp)
                    beta = min(beta, min_val)
                    if beta <= alpha:
                        break
                return min_val

            print('minimax_prune fail')

        return minimax_prune(state, -math.inf, math.inf)

    def alphabeta(self, state, alpha, beta):
        """This is just a helper method for minimax(). Feel free to use it or not."""
        pass


def get_agent(tag):
    if tag == 'random':
        return RandomAgent()
    elif tag == 'human':
        return HumanAgent()
    elif tag == 'mini':
        return MinimaxAgent()
    elif tag == 'prune':
        return MinimaxPruneAgent()
    elif tag.startswith('look'):
        depth = int(tag[4:])
        return MinimaxLookaheadAgent(depth)
    elif tag.startswith('alt'):
        depth = int(tag[3:])
        return AltMinimaxLookaheadAgent(depth)
    else:
        raise ValueError("bad agent tag: '{}'".format(tag))       

def streaks(lst):
    rets = []  # list of (element, length) tuples
    prev = lst[0]
    curr_len = 1
    for curr in lst[1:]:
        if curr == prev:
            curr_len += 1
        else:
            rets.append((prev, curr_len))
            prev = curr
            curr_len = 1
    rets.append((prev, curr_len))
    return rets