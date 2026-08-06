from __future__ import annotations

from typing import Any

import networkx as nx


class DependencyGraph:
    """
    Directed dependency graph for infrastructure components.

    Nodes represent infrastructure assets such as servers,
    services, databases, monitoring agents, etc.

    Directed edges represent dependency relationships.
    """

    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    # --------------------------------------------------
    # Component Operations
    # --------------------------------------------------

    def add_component(
        self,
        component_id: str,
        name: str,
        component_type: str,
        status: str = "Healthy",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Add a component to the dependency graph.
        """

        self.graph.add_node(
            component_id,
            name=name,
            type=component_type,
            status=status,
            metadata=metadata or {},
        )

    def remove_component(
        self,
        component_id: str,
    ) -> None:
        """
        Remove a component from the graph.
        """

        self.graph.remove_node(component_id)

    # --------------------------------------------------
    # Dependency Operations
    # --------------------------------------------------

    def add_dependency(
        self,
        source: str,
        target: str,
        dependency_type: str = "depends_on",
        weight: float = 1.0,
    ) -> None:
        """
        Create a directed dependency.

        source ---> target
        """

        self.graph.add_edge(
            source,
            target,
            dependency_type=dependency_type,
            weight=weight,
        )

    def remove_dependency(
        self,
        source: str,
        target: str,
    ) -> None:
        """
        Remove dependency edge.
        """

        self.graph.remove_edge(source, target)

    # --------------------------------------------------
    # Graph Queries
    # --------------------------------------------------

    def get_upstream(
        self,
        component_id: str,
    ) -> list[str]:
        """
        Components that this node depends on.
        """

        return list(
            self.graph.successors(component_id)
        )

    def get_downstream(
        self,
        component_id: str,
    ) -> list[str]:
        """
        Components depending on this node.
        """

        return list(
            self.graph.predecessors(component_id)
        )

    def shortest_path(
        self,
        source: str,
        target: str,
    ) -> list[str]:
        """
        Shortest dependency path.
        """

        return nx.shortest_path(
            self.graph,
            source,
            target,
        )

    def has_cycles(self) -> bool:
        """
        Check whether graph contains cycles.
        """

        return not nx.is_directed_acyclic_graph(
            self.graph
        )

    def affected_components(
        self,
        component_id: str,
    ) -> list[str]:
        """
        Return all downstream impacted components.
        """

        descendants = nx.ancestors(
            self.graph,
            component_id,
        )

        return sorted(descendants)

    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    def export_graph(self) -> dict[str, Any]:
        """
        Export graph structure.
        """

        return {
            "nodes": list(
                self.graph.nodes(data=True)
            ),
            "edges": list(
                self.graph.edges(data=True)
            ),
            "components": self.graph.number_of_nodes(),
            "dependencies": self.graph.number_of_edges(),
        }