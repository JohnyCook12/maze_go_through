"""
Find shortest path through the maze by breadth-first searching + backtracking.
O = start poing
F = finish
X = wall
' ' = route
"""

import copy
from collections import deque


def read_file(path):
    """
    Read a maze text file and split out each character. Return
    a 2-dimensional list where the first dimension is rows and
    the second is columns.
    """
    maze_list = []
    with open(path) as f:
        for line in f.read().splitlines():
            maze_list.append(list(line))
    return maze_list


def write_file(maze_list, path):
    """Write list of rows to file"""
    lines = ["".join(row)+'\n' for row in maze_list]

    with open(path, 'w') as f:
        f.writelines(lines)


def find_point(maze, point):
    """ Return coordinates of given point(character) """
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
    """ Breadt-first search from start to finish. Paths are written to 'visited' list as distance numbers """

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
    """ Write numbers from visited fields (distance) to original maze. For backtracking. """

    HEIGHT, LENGTH = len(maze), len(maze[1])
    maze_after = copy.deepcopy(maze)

    for r in range(HEIGHT):
        for c in range(LENGTH):
            # if maze_after[r][c] == ' ' and visited_fields[r][c] != False:
            if maze_after[r][c] == ' ' and visited_fields[r][c] != False:
                maze_after[r][c] = str(visited_fields[r][c])
            if maze_after[r][c] == 'O':
                maze_after[r][c] = '0'
        else:
            continue
    return maze_after


def replace_numbers_by_points(maze):
    """ Looks nicer """
    HEIGHT, LENGTH = len(maze), len(maze[1])

    for r in range(HEIGHT):
        for c in range(LENGTH):
            if maze[r][c] != ' ' and maze[r][c] != 'F' and maze[r][c] != '0' and maze[r][c] != 'X':
                maze[r][c] = '.'
        else:
            continue
    return maze


def backtrack(maze, path_length):
    """ Breadth first search from finish to start going only by nodes with decreasing numbers. """
    HEIGHT, LENGTH = len(maze), len(maze[1])
    start = find_point(maze, 'F')

    queue = deque()
    directions = [[0,1], [0,-1], [1,0], [-1,0]]

    'we add coordinates + distance from start'
    queue.appendleft((start[0], start[1], path_length))

    'array of visited coordinates'
    visited = [[False]*LENGTH for i in range(HEIGHT)]

    while len(queue) != 0:
        coord = queue.pop()
        visited[coord[0]][coord[1]] = coord[2]

        if maze[coord[0]][coord[1]] == '0':
            return visited

        for dir in directions:
            new_r, new_c = coord[0]+dir[0], coord[1]+dir[1]
            if (new_r < 0 or new_r >= HEIGHT or new_c < 0 or new_c >= LENGTH or maze[new_r][new_c] == 'X' or maze[new_r][new_c] == 'O' or
                 maze[new_r][new_c] == ' ' or visited[new_r][new_c] != False or int(maze[new_r][new_c]) >= coord[2]):
                continue
            queue.appendleft((new_r,new_c,coord[2]-1))

    return visited



maze = read_file("maze.txt")
shortest_path_length, visited_fields = solve_maze(maze)
maze_with_paths = mark_visited_path(maze, visited_fields)
shortest_path = backtrack(maze_with_paths, shortest_path_length)
shortest_path_in_maze = mark_visited_path(maze, shortest_path)
write_file(replace_numbers_by_points(shortest_path_in_maze), "maze_points.txt")




