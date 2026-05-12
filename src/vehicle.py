import networkx as nx


class Vehicle:

    def __init__(self, graph, start_node, goal_node):

        self.graph = graph

        self.start_node = start_node
        self.goal_node = goal_node

        # vehicle starts here initially
        self.current_node = start_node

        # calculate optimal route
        self.route = nx.shortest_path(
            self.graph,
            self.start_node,
            self.goal_node,
            weight='travel_time'
        )


    def get_route(self):
        return self.route

    def recalculateRoute(self):
        self.route = nx.shortest_path(
            self.graph,
            self.current_node,
            self.goal_node,
            weight='travel_time'
        )