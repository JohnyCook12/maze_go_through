"""
Find shortest path through the maze by breadth-first searching.
O = start poing
F = finish
X = wall
' ' = route
"""
import copy
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


def find_point(maze, point):
    HEIGHT, LENGTH = len(maze), len(maze[1])

    start = (0,0)
    for r in range(HEIGHT):
        for c in range(LENGTH):
            if maze[r][c] == point:
                start = (r,c)
                break
        else: continue
        break
    else:
        print('No point')
        return None
    return start


def solve_maze(maze):
    HEIGHT, LENGTH = len(maze), len(maze[1])
    start = find_point(maze, 'O')

    queue = deque()
    directions = [[0,1], [0,-1], [1,0], [-1,0]]

    'we add point + distance from start'
    queue.appendleft((start[0], start[1], 0))

    'array of visited coordinates'
    visited = [[False]*LENGTH for i in range(HEIGHT)]

    while len(queue) != 0:
        coord = queue.pop()
        visited[coord[0]][coord[1]] = coord[2]

        if maze[coord[0]][coord[1]] == 'F':
            print(f'Finished, shortest path is {coord[2]} steps')
            return coord[2], visited

        for dir in directions:
            new_r, new_c = coord[0]+dir[0], coord[1]+dir[1]
            if (new_r < 0 or new_r >= HEIGHT or new_c < 0 or new_c >= LENGTH or maze[new_r][new_c] == 'X' or maze[new_r][new_c] == 'O' or visited[new_r][new_c] != False):
                continue
            queue.appendleft((new_r,new_c,coord[2]+1))

    print(f'Didn´t reach the finish. Furthest path was {coord[2]} steps')
    return coord[2], visited


def mark_visited_path(maze, visited_fields):
    HEIGHT, LENGTH = len(maze), len(maze[1])
    maze_after = copy.deepcopy(maze)

    for r in range(HEIGHT):
        for c in range(LENGTH):
            # if maze_after[r][c] == ' ' and visited_fields[r][c] != False:
            if maze_after[r][c] == ' ' and visited_fields[r][c] != False:
                maze_after[r][c] = str(visited_fields[r][c])
            if maze_after[r][c] == 'O':
                maze_after[r][c] = '0'
        else: continue
        break
    return maze_after


def point_visited_path(maze):
    HEIGHT, LENGTH = len(maze), len(maze[1])

    for r in range(HEIGHT):
        for c in range(LENGTH):
            if maze[r][c] != ' ' and maze[r][c] != 'F' and maze[r][c] != '0' and maze[r][c] != 'X':
                maze[r][c] = '.'
        else: continue
        break
    return maze


def backtrack(maze, path_length):
    """
    Breadth first search from finish to start adding every node with lower mark to path.
    """
    HEIGHT, LENGTH = len(maze), len(maze[1])
    start = find_point(maze, 'F')

    queue = deque()
    directions = [[0,1], [0,-1], [1,0], [-1,0]]

    'we add point + distance from start'
    queue.appendleft((start[0], start[1], path_length))

    'array of visited coordinates'
    visited = [[False]*LENGTH for i in range(HEIGHT)]

    while len(queue) != 0:
        coord = queue.pop()
        visited[coord[0]][coord[1]] = coord[2]

        if maze[coord[0]][coord[1]] == '0':
            print(f'Finished, got back to step {coord[2]}')
            print('VISITED BACKTR', visited)
            return visited

        for dir in directions:
            new_r, new_c = coord[0]+dir[0], coord[1]+dir[1]
            if (new_r < 0 or new_r >= HEIGHT or new_c < 0 or new_c >= LENGTH or maze[new_r][new_c] == 'X' or maze[new_r][new_c] == 'O' or
                 maze[new_r][new_c] == ' ' or visited[new_r][new_c] != False or int(maze[new_r][new_c]) >= coord[2]):

                continue
            queue.appendleft((new_r,new_c,coord[2]-1))

    print(f'Didn´t reach the finish. Got back to step {coord[2]}')
    print('VISITED BACKTR', visited)
    return visited





maze = read_file("maze.txt")
shortest_path_length, visited_fields = solve_maze(maze)
print('visited_fields',visited_fields)
maze_after_breadth_first = mark_visited_path(maze, visited_fields)
write_file(maze_after_breadth_first, "maze_solved_breadt.txt")

track = backtrack(maze_after_breadth_first, shortest_path_length)
track_marked = mark_visited_path(maze, track)
write_file(track_marked, "maze_backtracked.txt")
write_file(point_visited_path(track_marked), "maze_maze_backtracked_points.txt")

# visited_fields_depth = depth_first_solve(maze_after_breadth_first, shortest_path_length)
# maze_after_depth_first = mark_visited_path(maze, visited_fields_depth)
# write_file(maze_after_depth_first, "maze_solved_depth.txt")




