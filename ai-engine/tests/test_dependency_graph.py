from __future__ import annotations

import pytest

from root_cause_analysis.dependency_graph import DependencyGraph


@pytest.fixture
def graph() -> DependencyGraph:
    g = DependencyGraph()

    g.add_component(
        "server1",
        "Application Server",
        "Server",
    )

    g.add_component(
        "service1",
        "Authentication Service",
        "Service",
    )

    g.add_component(
        "db1",
        "Primary Database",
        "Database",
    )

    return g


def test_add_component(graph: DependencyGraph):

    assert graph.graph.number_of_nodes() == 3

    assert "server1" in graph.graph.nodes

    assert graph.graph.nodes["server1"]["name"] == "Application Server"


def test_add_dependency(graph: DependencyGraph):

    graph.add_dependency(
        "server1",
        "service1",
    )

    graph.add_dependency(
        "service1",
        "db1",
    )

    assert graph.graph.number_of_edges() == 2


def test_upstream(graph: DependencyGraph):

    graph.add_dependency("server1", "service1")
    graph.add_dependency("service1", "db1")

    upstream = graph.get_upstream("server1")

    assert upstream == ["service1"]


def test_downstream(graph: DependencyGraph):

    graph.add_dependency("server1", "service1")
    graph.add_dependency("service1", "db1")

    downstream = graph.get_downstream("service1")

    assert downstream == ["server1"]


def test_shortest_path(graph: DependencyGraph):

    graph.add_dependency("server1", "service1")
    graph.add_dependency("service1", "db1")

    path = graph.shortest_path(
        "server1",
        "db1",
    )

    assert path == [
        "server1",
        "service1",
        "db1",
    ]


def test_cycle_detection(graph: DependencyGraph):

    graph.add_dependency("server1", "service1")
    graph.add_dependency("service1", "db1")

    assert graph.has_cycles() is False

    graph.add_dependency("db1", "server1")

    assert graph.has_cycles() is True


def test_remove_component(graph: DependencyGraph):

    graph.remove_component("db1")

    assert "db1" not in graph.graph.nodes


def test_remove_dependency(graph: DependencyGraph):

    graph.add_dependency(
        "server1",
        "service1",
    )

    graph.remove_dependency(
        "server1",
        "service1",
    )

    assert graph.graph.number_of_edges() == 0


def test_affected_components(graph: DependencyGraph):

    graph.add_dependency("server1", "service1")
    graph.add_dependency("service1", "db1")

    affected = graph.affected_components("db1")

    assert affected == [
        "server1",
        "service1",
    ]


def test_export_graph(graph: DependencyGraph):

    graph.add_dependency(
        "server1",
        "service1",
    )

    exported = graph.export_graph()

    assert exported["components"] == 3

    assert exported["dependencies"] == 1

    assert "nodes" in exported

    assert "edges" in exported