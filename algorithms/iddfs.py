import time

def iddfs(grid_obj):
    start_time=time.time()
    start, goal = grid_obj.start, grid_obj.goal

    def dls(node, depth, visited, came_from):
        if depth==0 and node==goal:
            return True
        if depth>0:
            visited.add(node)
            for n in grid_obj.get_neighbors(*node):
                if n not in visited:
                    came_from[n]=node
                    if dls(n, depth-1, visited, came_from):
                        return True
        return False

    max_depth=grid_obj.rows*grid_obj.cols
    for depth in range(max_depth):
        visited=set()
        came_from={}
        if dls(start, depth, visited, came_from):
            path=reconstruct_path(came_from,goal)
            elapsed=(time.time()-start_time)*1000
            return list(visited), path, len(visited), len(path), elapsed
    return [], [], 0, 0, 0

def reconstruct_path(came_from, current):
    path=[]
    while current in came_from:
        path.append(current)
        current=came_from[current]
    return path[::-1]
