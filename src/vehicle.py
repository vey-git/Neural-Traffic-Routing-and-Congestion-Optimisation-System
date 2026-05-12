import networkx as nx


class Vehicle:

    # =========================
    # INITIALISE VEHICLE
    # =========================

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

        # vehicle starts at start node
        self.current_node = start_node

        # selected routing algorithm
        self.algorithm = algorithm

        # =========================
        # INITIAL ROUTE
        # =========================

        if self.algorithm == "dijkstra":

            self.route = nx.shortest_path(

                self.graph,

                self.start_node,

                self.goal_node,

                weight='travel_time'

            )

        elif self.algorithm == "astar":

            self.route = nx.astar_path(

                self.graph,

                self.start_node,

                self.goal_node,

                heuristic=self.heuristic,

                weight='travel_time'

            )

        else:

            raise ValueError(
                "Algorithm must be 'dijkstra' or 'astar'"
            )

    # =========================
    # RETURN ROUTE
    # =========================

    def get_route(self):

        return self.route

    # =========================
    # RECALCULATE ROUTE
    # =========================

    def recalculateRoute(self):

        if self.algorithm == "dijkstra":

            self.route = nx.shortest_path(

                self.graph,

                self.current_node,

                self.goal_node,

                weight='travel_time'

            )

        elif self.algorithm == "astar":

            self.route = nx.astar_path(

                self.graph,

                self.current_node,

                self.goal_node,

                heuristic=self.heuristic,

                weight='travel_time'

            )

    # =========================
    # HEURISTIC FUNCTION
    # =========================

    def heuristic(self, node1, node2):

        # current node coordinates
        x1 = self.graph.nodes[node1]['x']
        y1 = self.graph.nodes[node1]['y']

        # goal node coordinates
        x2 = self.graph.nodes[node2]['x']
        y2 = self.graph.nodes[node2]['y']

        # Euclidean distance
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5