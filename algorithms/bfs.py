from collections import deque
import time

def bfs(grid_obj):
    start_time=time.time()
    start, goal = grid_obj.start, grid_obj.goal
    queue=deque([start])
    visited={start}
    came_from={}
    visited_list=[]

    while queue:
        current = queue.popleft()
        visited_list.append(current)
        if current==goal:
            path = reconstruct_path(came_from, current)
            elapsed=(time.time()-start_time)*1000
            return visited_list, path, len(visited_list), len(path), elapsed
        for n in grid_obj.get_neighbors(*current):
            if n not in visited:
                visited.add(n)
                came_from[n]=current
                queue.append(n)
    return visited_list, [], len(visited_list), 0, 0

def reconstruct_path(came_from, current):
    path=[]
    while current in came_from:
        path.append(current)
        current=came_from[current]
    return path[::-1]
