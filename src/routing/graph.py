import osmnx as os

from utils.config import (
    PLACE_NAME,
    NETWORK_TYPE
)


def create_graph():
    """
    Create drivable road network graph.
    """

    graph = os.graph_from_place(

        PLACE_NAME,

        network_type=NETWORK_TYPE

    )

    graph = os.add_edge_speeds(graph)

    graph = os.add_edge_travel_times(graph)

    for u, v, key, data in graph.edges(

        keys=True,
        data=True

    ):

        data[
            "base_travel_time"
        ] = data[
            "travel_time"
        ]

    return graph