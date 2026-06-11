import sys

sys.setrecursionlimit(5000)

class Node:
    def __init__(self, content: str) -> None:
        self.content = content

class Graph:
    def __init__(self):
        self.nodes: dict[Node, list[Node]] = {}

    def add_nodes(self, nodes: list[Node]) -> None:
        for node in nodes:
            self.nodes.update({node: []})

    def add_edges(self, edges: list[(Node, Node, int)]) -> None:
        for src, dst, cost in edges:
            self.nodes[src].append((dst, cost))
            self.nodes[dst].append((src, cost))

    def display_connections(self):
        for node in self.nodes:
            print(f"{node.content}: {[(n[0].content, n[1]) for n in self.nodes[node]]}")

    def dfs(self, adjancency_list: dict[Node, list[Node]]) -> None:
        visited = set()
        current = next(iter(adjancency_list))
        stack = [current]
        while (stack):
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            for node in adjancency_list[current]:
                if node not in visited:
                    stack.append(node)
            adjancency_list.pop(current)
        return adjancency_list

    def connected_components(self):
        copy = self.nodes
        count = 0
        while(copy):
            copy = self.dfs(copy)
            count += 1
        return count

    def dfs_with_recursion(self, current: Node) -> None:
        if current.visited:
            return
        current.visited = True
        for node in self.nodes[current]:
            if not node.visited:
                self.dfs(node)

    def bfs(self, adjancency_list: dict[Node, list[Node]]) -> list[Node] | None:
        start = next(iter(adjancency_list))
        end = list(adjancency_list.keys())[-1]
        path = []
        visited = set()
        queue = [start]
        parent = {}
        while (queue):
            current = queue.pop(0)
            if (current == end):
                path = [current.content]
                while(current != start):
                    current = parent[current]
                    path.insert(0, current.content)
                return path
            visited.add(current)
            for node in adjancency_list[current]:
                if node not in visited and node not in queue:
                    parent[node] = current
                    queue.append(node)

    def dungeon_problem(self, grid: list[list[Node]]) -> list[tuple[int, int]]:
        c = len(grid[0])
        r = len(grid)
        start = (0, 0)

        visited = set()
        queue = [start]
        parents = {}
        path = []
        while (queue):
            current = queue.pop(0)
            y, x = current
            if grid[y][x].content == "E":
                path = [current]
                while (current != start):
                    current = parents[current]
                    path.insert(0, current)
                return path
            visited.add((y, x))

            neighbors = [(y, x+1), (y, x-1), (y+1, x), (y-1, x)]
            for y, x in neighbors:
                if (0 <= x < c and 0 <= y < r 
                    and (y, x) not in visited 
                    and (y, x) not in queue
                    and grid[y][x].content != "#"):
                    queue.append((y, x))
                    parents[(y, x)] = current
        return []

    def  bfs_cost(self):
        visited = set()
        start = next(iter(self.nodes))
        queue = [(start, 0)]
        
        while (queue):
            current, cost = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            for node, c in self.nodes[current]:
                if node not in visited:
                    queue.append((node, cost + c))
            queue = sorted(queue, key=lambda x: x[1])



            
            

g = Graph()

nodes = [
    Node("A"), Node("B"), Node("C"),
    Node("D"), Node("E"),Node("F")
]
edges = [
    (nodes[0], nodes[1], 2), (nodes[0], nodes[3], 8),
    (nodes[1], nodes[3], 5), (nodes[1], nodes[4], 6),
    (nodes[2], nodes[4], 9), (nodes[-1], nodes[3], 2),
    (nodes[-1], nodes[4], 1), (nodes[-1], nodes[2], 3),
    (nodes[4], nodes[3], 3)
]

g.add_nodes(nodes)
g.add_edges(edges)

# g.display_connections()

g.bfs_cost()
# print(g.bfs(g.nodes))

# grid = [
#     [Node('S'), Node('.'), Node('.'), Node('#'), Node('.'), Node('.'), Node('.')],
#     [Node('.'), Node('#'), Node('.'), Node('.'), Node('.'), Node('#'), Node('.')],
#     [Node('.'), Node('#'), Node('.'), Node('.'), Node('.'), Node('.'), Node('.')],
#     [Node('.'), Node('.'), Node('#'), Node('#'), Node('.'), Node('.'), Node('.')],
#     [Node('#'), Node('.'), Node('#'), Node('E'), Node('.'), Node('#'), Node('.')],
# ]

# print(g.dungeon_problem(grid))
# print(g.connected_components())
# Graph.dfs(g.nodes, next(iter(g.nodes)))