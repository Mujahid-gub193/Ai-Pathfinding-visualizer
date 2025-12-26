import random
import heapq
import time
from collections import deque

class PathfindingGrid:
    def __init__(self, rows=20, cols=30):
        self.rows = rows
        self.cols = cols
        self.start = (2, 2)
        self.goal = (17, 27)
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.generate_random_walls()

    def generate_random_walls(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for _ in range(80):
            r, c = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if (r, c) != self.start and (r, c) != self.goal:
                self.grid[r][c] = 1

    def generate_easter_egg_maze(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                if (r+c) % 4 == 0 and (r, c) != self.start and (r, c) != self.goal:
                    self.grid[r][c] = 1

    def reset_visited(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] in [4, 5]:
                    self.grid[r][c] = 0

    def get_neighbors(self, r, c):
        neighbors = []
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<self.rows and 0<=nc<self.cols and self.grid[nr][nc]!=1:
                neighbors.append((nr,nc))
        return neighbors

    def heuristic(self, pos1, pos2):
        return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

    def bfs(self):
        start_time=time.time()
        queue=deque([self.start])
        visited={self.start}
        came_from={}
        visited_list=[]
        while queue:
            current=queue.popleft()
            visited_list.append(current)
            if current==self.goal:
                path=self.reconstruct_path(came_from,current)
                elapsed=(time.time()-start_time)*1000
                return visited_list, path, len(visited_list), len(path), elapsed
            for n in self.get_neighbors(*current):
                if n not in visited:
                    visited.add(n)
                    came_from[n]=current
                    queue.append(n)
        return visited_list, [], len(visited_list), 0, 0

    def dfs(self):
        start_time=time.time()
        stack=[self.start]
        visited={self.start}
        came_from={}
        visited_list=[]
        while stack:
            current=stack.pop()
            visited_list.append(current)
            if current==self.goal:
                path=self.reconstruct_path(came_from,current)
                elapsed=(time.time()-start_time)*1000
                return visited_list, path, len(visited_list), len(path), elapsed
            for n in self.get_neighbors(*current):
                if n not in visited:
                    visited.add(n)
                    came_from[n]=current
                    stack.append(n)
        return visited_list, [], len(visited_list), 0, 0

    def astar(self):
        start_time=time.time()
        open_set=[(0,self.start)]
        came_from={}
        g_score={self.start:0}
        visited=set()
        visited_list=[]
        while open_set:
            _, current=heapq.heappop(open_set)
            if current in visited: continue
            visited.add(current)
            visited_list.append(current)
            if current==self.goal:
                path=self.reconstruct_path(came_from,current)
                elapsed=(time.time()-start_time)*1000
                return visited_list, path, len(visited_list), len(path), elapsed
            for n in self.get_neighbors(*current):
                tentative_g=g_score[current]+1
                if n not in g_score or tentative_g<g_score[n]:
                    came_from[n]=current
                    g_score[n]=tentative_g
                    f_score=tentative_g+self.heuristic(n,self.goal)
                    heapq.heappush(open_set,(f_score,n))
        return visited_list, [], len(visited_list), 0, 0

    def iddfs(self):
        start_time=time.time()
        def dls(node,depth,visited,came_from):
            if depth==0 and node==self.goal: return True
            if depth>0:
                visited.add(node)
                for n in self.get_neighbors(*node):
                    if n not in visited:
                        came_from[n]=node
                        if dls(n,depth-1,visited,came_from):
                            return True
            return False
        max_depth=self.rows*self.cols
        for depth in range(max_depth):
            visited=set()
            came_from={}
            if dls(self.start,depth,visited,came_from):
                path=self.reconstruct_path(came_from,self.goal)
                elapsed=(time.time()-start_time)*1000
                visited_list=list(visited)
                return visited_list, path, len(visited_list), len(path), elapsed
        return [], [], 0, 0, 0

    def reconstruct_path(self, came_from, current):
        path=[]
        while current in came_from:
            path.append(current)
            current=came_from[current]
        return path[::-1]
