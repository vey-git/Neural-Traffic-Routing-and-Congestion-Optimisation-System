import networkx as nx


class Vehicle:
    """
    Vehicle routing object.
    """

    def __init__(

        self,
        graph,
        start_node,
        goal_node,
        algorithm="dijkstra"

    ):

        self.graph = graph

        self.start_node = start_node

        self.goal_node = goal_node

        self.current_node = start_node

        self.algorithm = algorithm

        self.nodes_explored = 0

        self.route = self.calculate_route()

    def calculate_route(self):

        if self.algorithm == "dijkstra":

            route = nx.shortest_path(

                self.graph,

                self.start_node,

                self.goal_node,

                weight="travel_time"

            )

        elif self.algorithm == "astar":

            route = nx.astar_path(

                self.graph,

                self.start_node,

                self.goal_node,

                heuristic=self.heuristic,

                weight="travel_time"

            )

        else:

            raise ValueError(
                "Unsupported routing algorithm."
            )

        self.nodes_explored = len(route)

        return route

    def recalculate_route(self):

        self.route = nx.shortest_path(

            self.graph,

            self.current_node,

            self.goal_node,

            weight="travel_time"

        )

    def heuristic(

        self,
        node1,
        node2

    ):

        x1 = self.graph.nodes[node1]["x"]
        y1 = self.graph.nodes[node1]["y"]

        x2 = self.graph.nodes[node2]["x"]
        y2 = self.graph.nodes[node2]["y"]

        return (
            (
                (x1 - x2) ** 2 +
                (y1 - y2) ** 2
            ) ** 0.5
        )