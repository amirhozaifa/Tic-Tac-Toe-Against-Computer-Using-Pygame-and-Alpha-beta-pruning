import copy

INF = 100000

# Next board from current state
next_board = []

def alpha_beta_pruning(state, player):
    """Runs Alpha-Beta Pruning on given state and player, returns the result."""
    
    if player == "Max":
        v = max_value(state, -INF, INF, True)
    else:
        v = min_value(state, -INF, INF, True)
    return v
    
def max_value(state, a, b, first_move):
    term, util = terminal_test_with_utility(state)
    if term:
        return util
    
    global next_board
    v = -INF
    next = successors(state, "Max")
    for s in next:
        w = min_value(s, a, b, False)
        if first_move and w > v:
            next_board = s
        v = max(v, w)
        if v >= b:
            return v
        a = max(a, v)
    return v
    
def min_value(state, a, b, first_move):
    term, util = terminal_test_with_utility(state)
    if term:
        return util
    
    global next_board
    v = INF
    next = successors(state, "Min")
    for s in next:
        w = max_value(s, a, b, False)
        if first_move and w < v:
            next_board = s
        v = min(v, w)
        if v <= a:
            return v
        b = min(b, v)
    return v
    
def successors(state, player):
    """Returns the successors from a given state."""
    
    next = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == "_":
                state[i][j] = "x" if player == "Max" else "o"
                next.append(copy.deepcopy(state))
                state[i][j] = "_"
    return next

def terminal_test_with_utility(state):
    """Tests if a state is terminal and returns utility value. Returns 1 for max, -1 for min and 0 for draw."""
    
    # Checking row 
    for i in range(3):
        if state[i][0] != '_' and state[i][0] == state[i][1] and state[i][1] == state[i][2]:
            return True, 1 if state[i][0] == 'x' else -1
        
    # Checking column 
    for j in range(3):
        if state[0][j] != '_' and state[0][j] == state[1][j] and state[1][j] == state[2][j]:
            return True, 1 if state[0][j] == 'x' else -1
        
    # Checking diagonal 
    if state[0][0] != '_' and state[0][0] == state[1][1] and state[1][1] == state[2][2]:
        return True, 1 if state[0][0] == 'x' else -1
    
    # Checking diagonal 
    if state[0][2] != '_' and state[0][2] == state[1][1] and state[1][1] == state[2][0]:
        return True, 1 if state[0][2] == 'x' else -1
    
    # Checking for empty cells
    for i in range(3):
        for j in range(3):
            if state[i][j] == "_":
                return False, None
    
    # No empty cells, hence utilty is 0
    return True, 0
    

result = 0

def is_complete(state, player = "Min"):
    global result
    term, util = terminal_test_with_utility(state)
    if term:
        win_util, lose_util = 0, 0
        if player == "Max":
            win_util, lose_util = 1, -1
        else:
            win_util, lose_util = -1, 1
            
        if util == win_util:
            result = -1
        elif util == lose_util:
            result = 1
        else:
            result = 0
        return True
    
    return False
    

def computer_move(state, player = "Min"):
    alpha_beta_pruning(state, player)
    return next_board

# def main():     
#     first_player = input("Will you go first? [Y/N] ").lower() == "n"
#     player = "Max" if first_player else "Min"
    
#     while True:
#         if first_player:
#             state = computer_move(state, player)
#             if is_complete(state, player):
#                 break
            
#         print("Your move:")
#         state.clear()        
#         for i in range(3):
#             state.append(input().split())
            
#         if is_complete(state, player):
#             break
            
#         if not first_player:
#             state = computer_move(state, player)
#             if is_complete(state, player):
#                 break                
    
