# class Node:
#     def __init__(self, name: str) -> None:
#         self.name = name
#         self.neighbors = []

#     def get_neighbors(self) -> list:
#         return [node for node in self.neighbors]


# class Graph:
#     def __init__(self) -> None:
#         self.nodes = {}

#     def add_node(self, node: Node) -> None:
#         self.nodes.update({node: node.neighbors})

#     def add_edge(self, node1: Node, node2: Node, cost: int) -> None:
#         node1.neighbors.append((node2, cost))

#     def diplay_nodes(self) -> None:
#         for node in self.nodes:
#             print(f"{node.name}: {node.get_neighbors()}")


# graph = Graph()
# a = Node('A')
# b = Node('B')
# c = Node('C')

# graph.add_node(a)
# graph.add_node(b)
# graph.add_node(c)

# graph.add_edge(a, b, 2)
# graph.add_edge(b, c, 9)

# graph.add_edge(b, a, 0)
# graph.add_edge(b, c, 8)

# graph.add_edge(c, b, 3)
# graph.add_edge(c, a, 10)
# graph.diplay_nodes()
