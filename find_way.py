"""
Find shortest path through the maze by breadth-first searching.
O = start poing
F = finish
X = wall
' ' = route
"""

from collections import deque


def read_file(path):
    """Read a maze text file and split out each character. Return
       a 2-dimensional list where the first dimension is rows and
       the second is columns."""
    maze_list = []
    with open(path) as f:
        for line in f.read().splitlines():
            maze_list.append(list(line))
    return maze_list


def write_file(maze_list, path):
    """Create file with path through maze"""
    lines = ["".join(row)+'\n' for row in maze_list]

    with open(path, 'w') as f:
        f.writelines(lines)


def solve_maze(maze):
    HEIGHT, LENGTH = len(maze), len(maze[1])

    start = (0,0)
    for r in range(HEIGHT):
        for c in range(LENGTH):
            if maze[r][c] == 'O':
                start = (r,c)
                break
        else: continue
        break
    else:
        print('No starting point')
        return None

    queue = deque()
    directions = [[0,1], [0,-1], [1,0], [-1,0]]

    'we add point + distance from start'
    queue.appendleft((start[0], start[1], 0))

    'array of visited coordinates'
    visited = [[False]*LENGTH for i in range(HEIGHT)]

    while len(queue) != 0:
        coord = queue.pop()
        visited[coord[0]][coord[1]] = True

        if maze[coord[0]][coord[1]] == 'F':
            print(f'Finished, shortest path is {coord[2]} steps')
            return coord[2], visited

        for dir in directions:
            new_r, new_c = coord[0]+dir[0], coord[1]+dir[1]
            if (new_r < 0 or new_r >= HEIGHT or new_c < 0 or new_c >= LENGTH or maze[new_r][new_c] == 'X' or visited[new_r][new_c]):
                continue
            queue.appendleft((new_r,new_c,coord[2]+1))

    print(f'Didn´t reach the finish. Furthest path was {coord[2]} steps')
    return coord[2], visited


def draw_path(maze, visited_fields):
    HEIGHT, LENGTH = len(maze), len(maze[1])
    maze_after = [['']*LENGTH for i in range(HEIGHT)]

    for r in range(HEIGHT):
        for c in range(LENGTH):
            maze_after[r][c] = str(maze[r][c])
            if maze[r][c] == ' ' and visited_fields[r][c] == True:
                maze_after[r][c] = '.'
        else: continue
        break
    return maze_after



maze = read_file("maze.txt")
shortest_path_length, visited_fields = solve_maze(maze)
# print(draw_path(maze, visited_fields))
write_file(draw_path(maze, visited_fields), "maze_solved.txt")





