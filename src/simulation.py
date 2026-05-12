import random
import networkx as nx
import matplotlib.pyplot as mpl
import osmnx as os
import time

from vehicle import Vehicle
from graph import createGraph

from metrics import (
    calculateEdgeUsage,
    calculateAverageEdgeUsage,
    calculateMaxEdgeUsage,
    calculateTotalTravelCost,
    calculateAverageTravelCost,
    calculateRouteChanges,
    countCongestionLevels,
    updateCongestionWeights,
    exportResultsCSV
)



def runSimulation(num_of_vehicles):
    start_time = time.time() #starts the runtime of the program.
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
                vehicle.original_route = vehicle.route.copy()
                vehicles.append(vehicle)

                print(f"Vehicle {i + 1} Created")

                valid_route = True

            except nx.NetworkXNoPath:

                print("Invalid route... retrying")
    edge_count_before = calculateEdgeUsage(vehicles)

    #create variables before rerouting
    average_before = calculateAverageEdgeUsage(
        edge_count_before
    )

    max_before = calculateMaxEdgeUsage(
        edge_count_before
    )

    total_cost_before = calculateTotalTravelCost(
        G,
        vehicles
    )

    average_cost_before = calculateAverageTravelCost(
        G,
        vehicles
    )

    congestion_before = countCongestionLevels(
        edge_count_before,
        average_before
    )

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
    vehicle.original_route = vehicle.route.copy() #store a copy for measuring metrics
    changed_routes = 0

    for vehicle in vehicles:

        old_route = vehicle.route.copy()

        vehicle.recalculateRoute()

        if old_route != vehicle.route:

            changed_routes += 1

    print(f"Vehicles Rerouted: {changed_routes}")

    #recalculate metrics based on rerouting
    edge_count_after = calculateEdgeUsage(
        vehicles
    )

    average_after = calculateAverageEdgeUsage(
        edge_count_after
    )

    max_after = calculateMaxEdgeUsage(
        edge_count_after
    )

    total_cost_after = calculateTotalTravelCost(
        G,
        vehicles
    )

    average_cost_after = calculateAverageTravelCost(
        G,
        vehicles
    )

    congestion_after = countCongestionLevels(
        edge_count_after,
        average_after
    )

    rerouted_vehicles = calculateRouteChanges(
        vehicles
    )
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

    end_time = time.time()

    runtime = end_time - start_time #final runtime

    # =========================
    # Metrics
    # =========================

    print(f"-------Metric Results-------\n")

    print(f"Vehicles Simulated: {num_of_vehicles}")

    print(f"Average Edge Usage: {average_after}")
    print(f"Maximum Edge Usage: {max_after}")

    print(f"Total Travel Cost: {total_cost_after}")
    print(f"Average Travel Cost: {average_cost_after}")

    print(f"Vehicles Rerouted: {rerouted_vehicles}")

    print(f"Runtime: {runtime:.2f} seconds")

    print("\n===== CONGESTION DISTRIBUTION =====")

    print(f"Green Edges: {congestion_after['green']}")
    print(f"Yellow Edges: {congestion_after['yellow']}")
    print(f"Orange Edges: {congestion_after['orange']}")
    print(f"Red Edges: {congestion_after['red']}")

    # =========================
    # Export results
    # =========================

    exportResultsCSV([

        num_of_vehicles,
        True,

        average_after,
        max_after,

        total_cost_after,
        average_cost_after,

        congestion_after['green'],
        congestion_after['yellow'],
        congestion_after['orange'],
        congestion_after['red'],

        rerouted_vehicles,

        runtime
    ])