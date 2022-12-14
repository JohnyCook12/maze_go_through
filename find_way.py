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


def mark_visited_path(maze, visited_fields):
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


def depth_first_solve(maze):
    """
    Now we go from finish to start and use only fields previously visited.


    """

    HEIGHT, LENGTH = len(maze), len(maze[1])
    start = find_point(maze, 'F')

    queue_prim = deque()
    queue_sec = deque()
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    'we add point + distance from start'
    queue_sec.appendleft((start[0], start[1], 0))

    'array of visited coordinates'
    visited = [[False] * LENGTH for i in range(HEIGHT)]

    while len(queue_sec) != 0:
        another_branch_beginning = queue_sec.pop()
        queue_prim.append(another_branch_beginning)

        while len(queue_prim) != 0:
            coord = queue_prim.pop()

            visited[coord[0]][coord[1]] = True

            if maze[coord[0]][coord[1]] == 'O':
                print(f'Depth-first finished, shortest path is {coord[2]} steps')
                return visited

            first_branch_appended = 0
            for dir in directions:
                new_r, new_c = coord[0] + dir[0], coord[1] + dir[1]
                if (new_r < 0 or new_r >= HEIGHT or new_c < 0 or new_c >= LENGTH or maze[new_r][new_c] == 'X' or
                        visited[new_r][new_c] or maze[new_r][new_c] == ' '):
                    continue
                if first_branch_appended == 0:
                    queue_prim.append((new_r, new_c, coord[2] + 1))
                    first_branch_appended = 1
                else:
                    queue_sec.append((new_r, new_c, coord[2] + 1))
            # first_branch_appended = 0

    print(f'Didn´t reach the finish. Furthest path was {coord[2]} steps')
    return visited



maze = read_file("maze.txt")
shortest_path_length, visited_fields = solve_maze(maze)
# print(draw_path(maze, visited_fields))
maze_after_breadth_first = mark_visited_path(maze, visited_fields)
write_file(maze_after_breadth_first, "maze_solved_breadt.txt")

visited_fields_depth = depth_first_solve(maze_after_breadth_first)
maze_after_depth_first = mark_visited_path(maze, visited_fields_depth)
write_file(maze_after_depth_first, "maze_solved_depth.txt")





