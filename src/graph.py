import osmnx as os


def createGraph():

    G = os.graph_from_place(
        "Oxford, England",
        network_type="drive"
    )

    G = os.add_edge_speeds(G)
    G = os.add_edge_travel_times(G)

    # store original travel times
    for u, v, key, data in G.edges(keys=True, data=True):

        data['base_travel_time'] = data['travel_time']

    return G