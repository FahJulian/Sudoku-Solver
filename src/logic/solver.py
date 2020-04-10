from typing import List, Optional


def solve(board: List[List[int]], log_list: Optional[List] = None) -> Optional[List[List[int]]]:
    ''' Solves a sudoku board using backtracking '''
    pos = _next_empty_pos(board)
    if not pos: return board    # No empty pos -> Board is solved

    row, col = pos
    for num in range(1, 10):
        if _num_valid_at_pos(board, pos, num):
            if log_list != None: _log(log_list, 'PUT', pos, num)
            board[row][col] = num
            solution = solve(board, log_list)

            if solution:
                return solution
            else:
                board[row][col] = 0
        else:
            if log_list != None: _log(log_list, 'INVALID', pos, num)
    else:
        if log_list != None: _log(log_list, 'REMOVE', pos, None)
        return None

def _log(log_list, action: str, pos: List[int], num: int) -> None:
    '''
    Appends a dictionary that representates a log entry to the log list
    '''
    log_list.append({
        'action': action,
        'pos': pos,
        'num': num,
    })

def _next_empty_pos(board: List[int]) -> Optional[List[int]]:
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0: 
                return (row, col)
    else:
        return None

def _num_valid_at_pos(board: List[List[int]], pos: List[int], num: int) -> bool:
    for row in range(9):
        for col in range(9):
            if (row, col) == pos: continue
            relevant = False

            # Same row or col
            if row == pos[0] or col == pos[1]: 
                relevant = True
            # Same 3x3 field
            if (row // 3 == pos[0] // 3) and (col // 3 == pos[1] // 3):
                relevant = True

            if relevant and num == board[row][col]:
                return False
    else:
        return True
