#
def get_valid_neighbors(cell, board, rows, cols):
    x,y = cell
    neighbors = []
    if abs(board[x][y]) == 4:
        return neighbors
    if y < len(board[0])-1  and abs(board[x][y + 1]) <= 3 and cols[x][y + 1] != 1:
        neighbors.append((x, y + 1))
    if y > 0 and abs(board[x][y - 1]) <= 3 and cols[x][y] != 1:
        neighbors.append((x, y - 1))
    if x < len(board)-1 and abs(board[x + 1][y]) <= 3 and rows[x + 1][y] != 1:
        neighbors.append((x + 1, y))
    if x > 0 and abs(board[x][y]) <= 3 and rows[x][y] != 1:
        neighbors.append((x - 1, y))
    return neighbors


def dfs(cell, board, rows, cols, visited, chain):
    visited.add(cell)
    chain.append(cell)

    neighbors = get_valid_neighbors(cell, board, rows, cols)

    if len(neighbors) == 0 or set(neighbors) <= visited:
        return True

    for neighbor in neighbors:
        if neighbor not in visited:
            x, y = neighbor
            if abs(board[x][y]) == 4:
                return True
            elif abs(board[x][y]) <= 3:
                if dfs(neighbor, board, rows, cols, visited, chain):
                    return True


def find_chains(board, rows, cols):
    chains = []
    visited = set()

    for row in range(len(board)):
        for col in range(len(board[0])):
            cell = (row, col)
            if abs(board[row][col]) <= 3 and cell not in visited:
                chain = []
                if dfs(cell, board, rows, cols, visited, chain):
                    chains.append(chain)

    return chains

# Esempio di utilizzo:
board = [
    [-2, 2, -2, -2, 2],
    [2, -1, 2, 2, -2],
    [-2, 2, 2, -2, 2],
    [-2, -2, 2, -2, -2],
    [-2, 2, -2, 2, -2]
]

rows = [
    [1, 1, 1, 1, 0],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0],
    [1, 1, 0, 0, 1]
]

cols = [
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1],
    [0, 1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1]
]



neig = find_chains(board, rows, cols)
#neig = get_valid_neighbors((1,1), board, rows, cols)
print(len(neig))
print(neig)
