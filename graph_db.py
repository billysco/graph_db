from typing import Dict, Any, Set

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def validate_node_id(self, node_id: str) -> None:
        """Validate that a node exists."""
        if not isinstance(node_id, str):
            raise TypeError("Node ID must be a string")
        if node_id not in self.nodes:
            raise ValueError(f"Node '{node_id}' does not exist")

    def add_node(self, node_id: str, **properties: Any) -> None:
        if not isinstance(node_id, str):
            raise TypeError("Node ID must be a string")
        if node_id not in self.nodes:
            self.nodes[node_id] = properties
            self.edges[node_id] = {}
        else:
            self.nodes[node_id].update(properties)

    def add_edge(self, from_node: str, to_node: str, bidirectional: bool = False, **properties: Any) -> None:
        if from_node not in self.nodes or to_node not in self.nodes:
            raise ValueError("Both nodes must exist before adding an edge.")
        self.edges[from_node][to_node] = properties
        if bidirectional:
            self.edges[to_node][from_node] = properties.copy() 
            
    def get_neighbors(self, node_id: str) -> Set[str]:
        return set(self.edges.get(node_id, {}).keys())

    def get_node_properties(self, node_id: str) -> Dict[str, Any]:
        return self.nodes.get(node_id, {})

    def get_edge_properties(self, from_node: str, to_node: str) -> Dict[str, Any]:
        return self.edges.get(from_node, {}).get(to_node, {})

    def remove_node(self, node_id: str) -> None:
        """Remove a node and all its associated edges."""
        if node_id in self.nodes:
            # Remove all edges pointing to this node
            for node in self.edges:
                self.edges[node].pop(node_id, None)
            # Remove the node and its edges
            self.edges.pop(node_id, None)
            self.nodes.pop(node_id)

    def remove_edge(self, from_node: str, to_node: str) -> None:
        """Remove an edge between two nodes."""
        if from_node in self.edges:
            self.edges[from_node].pop(to_node, None)

    def get_all_paths(self, start: str, end: str, path: list = None) -> list:
        """Find all paths between two nodes."""
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.edges:
            return []
        paths = []
        for node in self.edges[start]:
            if node not in path:
                new_paths = self.get_all_paths(node, end, path)
                paths.extend(new_paths)
        return paths

    def shortest_path(self, start: str, end: str) -> list:
        """Find shortest path between two nodes."""
        all_paths = self.get_all_paths(start, end)
        if not all_paths:
            return []
        return min(all_paths, key=len)

# Example usage:
# g = Graph()
# g.add_node("Alice", age=30, occupation="Data Scientist")
# g.add_node("Bob", age=25, occupation="Engineer")
# g.add_edge("Alice", "Bob", relation="knows")

# print(g.get_neighbors("Alice"))  # Should print: dict_keys(['Bob'])
