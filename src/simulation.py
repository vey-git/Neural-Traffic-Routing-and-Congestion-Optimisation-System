import random
import networkx as nx
import matplotlib.pyplot as mpl
import osmnx as os

from vehicle import Vehicle
from graph import createGraph

from metrics import (
    calculateEdgeUsage,
    calculateAverageEdgeUsage,
    updateCongestionWeights
)



def runSimulation(num_of_vehicles):

    # =========================
    # CREATE GRAPH
    # =========================

    G = createGraph()

    Nodes = list(G.nodes)

    # =========================
    # GENERATE VEHICLES
    # =========================

    vehicles = []

    for i in range(num_of_vehicles):

        valid_route = False

        while not valid_route:

            random_start = random.choice(Nodes)
            random_goal = random.choice(Nodes)

            while random_start == random_goal:
                random_goal = random.choice(Nodes)

            try:

                vehicle = Vehicle(
                    G,
                    random_start,
                    random_goal
                )

                vehicles.append(vehicle)

                print(f"Vehicle {i + 1} Created")

                valid_route = True

            except nx.NetworkXNoPath:

                print("Invalid route... retrying")

    # =========================
    # INITIAL CONGESTION
    # =========================

    edge_count_before = calculateEdgeUsage(vehicles)

    average_before = calculateAverageEdgeUsage(
        edge_count_before
    )

    print(f"Average Edge Usage BEFORE: {average_before}")

    # =========================
    # UPDATE WEIGHTS
    # =========================

    updateCongestionWeights(
        G,
        edge_count_before,
        average_before
    )

    # =========================
    # REROUTE VEHICLES
    # =========================

    changed_routes = 0

    for vehicle in vehicles:

        old_route = vehicle.route.copy()

        vehicle.recalculateRoute()

        if old_route != vehicle.route:

            changed_routes += 1

    print(f"Vehicles Rerouted: {changed_routes}")

    # =========================
    # NEW CONGESTION
    # =========================

    edge_count_after = calculateEdgeUsage(vehicles)

    average_after = calculateAverageEdgeUsage(
        edge_count_after
    )

    print(f"Average Edge Usage AFTER: {average_after}")

    # =========================
    # VISUALISATION
    # =========================

    edge_colours = []
    edge_widths = []

    for u, v, key in G.edges(keys=True):

        usage = 0

        if (u, v) in edge_count_after:
            usage = edge_count_after[(u, v)]

        if usage < average_after * 0.5:

            edge_colours.append("lime")
            edge_widths.append(0.5)

        elif usage < average_after:

            edge_colours.append("yellow")
            edge_widths.append(1)

        elif usage < average_after * 1.5:

            edge_colours.append("orange")
            edge_widths.append(2)

        else:

            edge_colours.append("red")
            edge_widths.append(3)

    fig, ax = os.plot_graph(
        G,
        node_size=0,
        edge_color=edge_colours,
        edge_linewidth=edge_widths,
        bgcolor='black',
        show=False,
        close=False
    )

    ax.set_title(
        "Oxford Traffic Congestion Simulation",
        fontsize=18,
        color='white',
        pad=20
    )

    # plot vehicles
    for vehicle in vehicles:

        ax.scatter(
            G.nodes[vehicle.current_node]['x'],
            G.nodes[vehicle.current_node]['y'],
            color='cyan',
            s=15,
            zorder=10
        )

    mpl.show()