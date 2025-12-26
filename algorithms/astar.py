import heapq, time

def astar(grid_obj):
    start_time=time.time()
    start, goal = grid_obj.start, grid_obj.goal
    open_set=[(0,start)]
    came_from={}
    g_score={start:0}
    visited=set()
    visited_list=[]

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in visited: continue
        visited.add(current)
        visited_list.append(current)
        if current==goal:
            path=reconstruct_path(came_from,current)
            elapsed=(time.time()-start_time)*1000
            return visited_list, path, len(visited_list), len(path), elapsed
        for n in grid_obj.get_neighbors(*current):
            tentative_g=g_score[current]+1
            if n not in g_score or tentative_g<g_score[n]:
                came_from[n]=current
                g_score[n]=tentative_g
                f_score=tentative_g+heuristic(n,goal)
                heapq.heappush(open_set,(f_score,n))
    return visited_list, [], len(visited_list), 0, 0

def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def reconstruct_path(came_from,current):
    path=[]
    while current in came_from:
        path.append(current)
        current=came_from[current]
    return path[::-1]
