import random
import time

import networkx as nx

from routing.graph import create_graph

from routing.metrics import (

    calculate_average_edge_usage,

    calculate_average_travel_cost,

    calculate_edge_usage,

    calculate_max_edge_usage,

    calculate_route_changes,

    calculate_total_travel_cost,

    count_congestion_levels,

    export_results_csv,

    export_training_data,

    update_congestion_weights
)

from routing.vehicle import Vehicle

from visualisation.visualisation import (
    plot_congestion_heatmap
)


# ==========================================================
# VEHICLE GENERATION
# ==========================================================

def generate_vehicles(
    graph,
    num_vehicles,
    algorithm
):
    """
    Generate vehicles with valid routes.
    """

    vehicles = []

    graph_nodes = list(graph.nodes)

    total_nodes_explored = 0

    print(f"Generating {num_vehicles} vehicles...")

    for vehicle_index in range(num_vehicles):

        valid_route = False

        while not valid_route:

            start_node = random.choice(
                graph_nodes
            )

            destination_node = random.choice(
                graph_nodes
            )

            while start_node == destination_node:

                destination_node = random.choice(
                    graph_nodes
                )

            try:

                vehicle = Vehicle(

                    graph,

                    start_node,

                    destination_node,

                    algorithm=algorithm
                )

                vehicle.original_route = (
                    vehicle.route.copy()
                )

                vehicles.append(vehicle)

                total_nodes_explored += (
                    vehicle.nodes_explored
                )

                print(
                    f"Vehicle {vehicle_index + 1} created"
                )

                valid_route = True

            except nx.NetworkXNoPath:

                print(
                    "Invalid route detected. Retrying..."
                )

    average_nodes_explored = (

        total_nodes_explored /

        max(num_vehicles, 1)
    )

    return vehicles, average_nodes_explored


# ==========================================================
# MAIN SIMULATION
# ==========================================================

def run_simulation(

    num_vehicles,

    algorithm,

    use_neural_network=False
):
    """
    Run congestion-routing simulation.
    """

    print("\nStarting simulation...\n")

    simulation_start = time.time()

    # ======================================================
    # CREATE GRAPH
    # ======================================================

    graph = create_graph()

    # ======================================================
    # GENERATE VEHICLES
    # ======================================================

    vehicles, average_nodes_explored = (

        generate_vehicles(

            graph,

            num_vehicles,

            algorithm
        )
    )

    # ======================================================
    # INITIAL EDGE USAGE
    # ======================================================

    edge_usage_before = (
        calculate_edge_usage(
            vehicles
        )
    )

    average_usage_before = (

        calculate_average_edge_usage(
            edge_usage_before
        )
    )

    # ======================================================
    # APPLY CONGESTION WEIGHTS
    # ======================================================

    update_congestion_weights(

        graph,

        edge_usage_before,

        average_usage_before,

        use_neural_network
    )

    # ======================================================
    # HEATMAP BEFORE REROUTING
    # ======================================================

    plot_congestion_heatmap(

        graph,

        edge_usage_before,

        average_usage_before,

        f"{algorithm}_before_rerouting",

        num_vehicles,

        vehicles
    )

    # ======================================================
    # REROUTE VEHICLES
    # ======================================================

    print("\nRecalculating routes...\n")

    for vehicle in vehicles:

        try:

            vehicle.recalculate_route()

        except nx.NetworkXNoPath:

            continue

    # ======================================================
    # UPDATED EDGE USAGE
    # ======================================================

    edge_usage_after = (
        calculate_edge_usage(
            vehicles
        )
    )

    average_usage_after = (

        calculate_average_edge_usage(
            edge_usage_after
        )
    )

    # ======================================================
    # HEATMAP AFTER REROUTING
    # ======================================================

    plot_congestion_heatmap(

        graph,

        edge_usage_after,

        average_usage_after,

        f"{algorithm}_after_rerouting",

        num_vehicles,

        vehicles
    )

    # ======================================================
    # EXPORT TRAINING DATA
    # ======================================================

    export_training_data(
        graph,
        edge_usage_after,
        average_usage_after
    )

    # ======================================================
    # SIMULATION RUNTIME
    # ======================================================

    runtime_seconds = (

        time.time() -

        simulation_start
    )

    # ======================================================
    # CONGESTION DISTRIBUTION
    # ======================================================

    congestion_distribution = (

        count_congestion_levels(

            edge_usage_after,

            average_usage_after
        )
    )

    # ======================================================
    # EXPORT RESULTS
    # ======================================================

    export_results_csv([

        num_vehicles,

        algorithm,

        (
            "neural_network"
            if use_neural_network
            else "static"
        ),

        True,

        average_usage_after,

        calculate_max_edge_usage(
            edge_usage_after
        ),

        calculate_total_travel_cost(
            graph,
            vehicles
        ),

        calculate_average_travel_cost(
            graph,
            vehicles
        ),

        congestion_distribution["green"],

        congestion_distribution["yellow"],

        congestion_distribution["orange"],

        congestion_distribution["red"],

        calculate_route_changes(
            vehicles
        ),

        runtime_seconds,

        average_nodes_explored
    ])

    # ======================================================
    # SUMMARY OUTPUT
    # ======================================================

    print("\n===== SIMULATION SUMMARY =====")

    print(
        f"Vehicles: {num_vehicles}"
    )

    print(
        f"Algorithm: {algorithm}"
    )

    print(
        f"Average Edge Usage: "
        f"{average_usage_after:.2f}"
    )

    print(
        f"Maximum Edge Usage: "
        f"{calculate_max_edge_usage(edge_usage_after)}"
    )

    print(
        f"Rerouted Vehicles: "
        f"{calculate_route_changes(vehicles)}"
    )

    print(
        f"Runtime: "
        f"{runtime_seconds:.2f} seconds"
    )

    print("\nSimulation complete.\n")