import random
import networkx as nx
import time

from vehicle import Vehicle
from graph import createGraph

from src.main_program.visualisation import (
    plotCongestionHeatmap
)

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


# =========================
# RUN SIMULATION
# =========================

def runSimulation(
    num_of_vehicles,
    algorithm
):

    # =========================
    # START TIMER
    # =========================

    start_time = time.time()

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

                # =========================
                # CREATE VEHICLE
                # =========================

                vehicle = Vehicle(

                    G,

                    random_start,

                    random_goal,

                    algorithm=algorithm
                )

                # store original route
                vehicle.original_route = vehicle.route.copy()

                vehicles.append(vehicle)

                print(f"Vehicle {i + 1} Created")

                valid_route = True

            except nx.NetworkXNoPath:

                print("Invalid route... retrying")

    # =========================
    # INITIAL METRICS
    # =========================

    edge_count_before = calculateEdgeUsage(
        vehicles
    )

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

    print(
        f"Average Edge Usage BEFORE: {average_before}"
    )

    # =========================
    # UPDATE CONGESTION
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

    print(
        f"Vehicles Rerouted: {changed_routes}"
    )

    # =========================
    # POST-REROUTE METRICS
    # =========================

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

    print(
        f"Average Edge Usage AFTER: {average_after}"
    )

    # =========================
    # END TIMER
    # =========================

    end_time = time.time()

    runtime = end_time - start_time

    # =========================
    # HEATMAP
    # =========================

    plotCongestionHeatmap(

        G,

        edge_count_after,

        average_after,

        algorithm,

        num_of_vehicles,

        vehicles
    )

    # =========================
    # METRICS OUTPUT
    # =========================

    print("\n======= METRIC RESULTS =======\n")

    print(
        f"Vehicles Simulated: {num_of_vehicles}"
    )

    print(
        f"Algorithm: {algorithm}"
    )

    print(
        f"Average Edge Usage: {average_after}"
    )

    print(
        f"Maximum Edge Usage: {max_after}"
    )

    print(
        f"Total Travel Cost: {total_cost_after}"
    )

    print(
        f"Average Travel Cost: {average_cost_after}"
    )

    print(
        f"Vehicles Rerouted: {rerouted_vehicles}"
    )

    print(
        f"Runtime: {runtime:.2f} seconds"
    )

    print("\n===== CONGESTION DISTRIBUTION =====")

    print(
        f"Green Edges: {congestion_after['green']}"
    )

    print(
        f"Yellow Edges: {congestion_after['yellow']}"
    )

    print(
        f"Orange Edges: {congestion_after['orange']}"
    )

    print(
        f"Red Edges: {congestion_after['red']}"
    )

    # =========================
    # EXPORT RESULTS
    # =========================

    exportResultsCSV([

        num_of_vehicles,

        algorithm,

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