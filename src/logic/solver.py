def solve(board, log_list=None):
    '''
    Solves a sudoku board using backtracking
    :param board: int[][]
    :param log_list: Pointer to a list to append logging entries to
    :return: int[][] or None
    '''
    pos = _next_empty_pos(board)
    if not pos: return board    # No empty pos -> Board is solved

    row, col = pos
    for num in range(1, 10):
        if _num_valid_at_pos(board, pos, num):
            _log(log_list, 'PUT', pos, num)
            board[row][col] = num
            solution = solve(board)

            if solution:
                return solution
            else:
                board[row][col] = 0
        else:
            _log(log_list, 'INVALID', pos, num)
    else:
        _log(log_list, 'REMOVE', pos, None)
        return None

def _log(log_list, action, pos, num):
    '''
    Appends a dictionary that representates a log entry to the log list
    '''
    log_list.append({
        'action': action,
        'pos': pos,
        'num': num,
    })

def _next_empty_pos(board):
    '''
    :param board: int[][]
    :return: int[] or None
    '''
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0: 
                return (row, col)
    else:
        return None

def _num_valid_at_pos(board, pos, num):
    '''
    :param board: int[][]
    :param pos: int[]
    :param num: int
    :return: bool
    '''
    for row in range(9):
        for col in range(9):
            if (row, col) == pos: continue
            relevant = False

            # Same row or col
            if row == pos[0] or col == pos[1]: 
                relevant = True
            # Same 3x3 field
            if (row // 3 == pos[0] // 3) or (col // 3 == pos[1] // 3):
                relevant = True

            if relevant and num == board[row][col]:
                return False
    else:
        return True
