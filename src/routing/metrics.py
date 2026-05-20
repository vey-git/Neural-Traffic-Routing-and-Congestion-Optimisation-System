import csv

import networkx as nx

from neural_network.inference import (
    predict_congestion
)

from utils.config import (

    ROAD_TYPE_MAPPING,

    TRAINING_DATA_PATH,

    RESULTS_CSV_PATH
)


# ==========================================================
# EDGE USAGE ANALYSIS
# ==========================================================

def calculate_edge_usage(vehicles):
    """
    Count how frequently each edge
    is traversed by vehicles.
    """

    edge_usage = {}

    for vehicle in vehicles:

        route = vehicle.route

        for index in range(len(route) - 1):

            edge = (
                route[index],
                route[index + 1]
            )

            edge_usage[edge] = (
                edge_usage.get(edge, 0) + 1
            )

    return edge_usage


# ==========================================================
# AVERAGE EDGE USAGE
# ==========================================================

def calculate_average_edge_usage(edge_usage):
    """
    Calculate average edge utilisation.
    """

    if len(edge_usage) == 0:

        return 0

    total_usage = sum(edge_usage.values())

    return total_usage / len(edge_usage)


# ==========================================================
# MAXIMUM EDGE USAGE
# ==========================================================

def calculate_max_edge_usage(edge_usage):
    """
    Return maximum edge utilisation.
    """

    if len(edge_usage) == 0:

        return 0

    return max(edge_usage.values())


# ==========================================================
# TOTAL TRAVEL COST
# ==========================================================

def calculate_total_travel_cost(
    graph,
    vehicles
):
    """
    Calculate cumulative travel cost.
    """

    total_cost = 0

    for vehicle in vehicles:

        route_cost = nx.path_weight(

            graph,

            vehicle.route,

            weight="travel_time"
        )

        total_cost += route_cost

    return total_cost


# ==========================================================
# AVERAGE TRAVEL COST
# ==========================================================

def calculate_average_travel_cost(
    graph,
    vehicles
):
    """
    Calculate average travel cost.
    """

    if len(vehicles) == 0:

        return 0

    total_cost = calculate_total_travel_cost(

        graph,

        vehicles
    )

    return total_cost / len(vehicles)


# ==========================================================
# CONGESTION DISTRIBUTION
# ==========================================================

def count_congestion_levels(
    edge_usage,
    average_edge_usage
):
    """
    Categorise congestion severity.
    """

    congestion_counts = {

        "green": 0,
        "yellow": 0,
        "orange": 0,
        "red": 0
    }

    for usage in edge_usage.values():

        if usage < average_edge_usage * 0.5:

            congestion_counts["green"] += 1

        elif usage < average_edge_usage:

            congestion_counts["yellow"] += 1

        elif usage < average_edge_usage * 1.5:

            congestion_counts["orange"] += 1

        else:

            congestion_counts["red"] += 1

    return congestion_counts


# ==========================================================
# ROUTE CHANGE ANALYSIS
# ==========================================================

def calculate_route_changes(vehicles):
    """
    Count vehicles that changed route.
    """

    changed_routes = 0

    for vehicle in vehicles:

        if vehicle.original_route != vehicle.route:

            changed_routes += 1

    return changed_routes


# ==========================================================
# CONGESTION WEIGHTING
# ==========================================================

def update_congestion_weights(

    graph,

    edge_usage,

    average_edge_usage,

    use_neural_network=False
):
    """
    Apply congestion-adjusted
    travel time weighting.
    """

    for edge, usage in edge_usage.items():

        u, v = edge

        if not graph.has_edge(u, v):

            continue

        edge_data = graph[u][v]

        for key in edge_data:

            data = edge_data[key]

            base_travel_time = data.get(
                "base_travel_time",
                1
            )

            road_length = data.get(
                "length",
                0
            )

            speed_limit = data.get(
                "speed_kph",
                30
            )

            if isinstance(speed_limit, list):

                speed_limit = speed_limit[0]

            road_type = data.get(
                "highway",
                "residential"
            )

            if isinstance(road_type, list):

                road_type = road_type[0]

            road_type_encoded = (
                ROAD_TYPE_MAPPING.get(
                    road_type,
                    5
                )
            )

            nearby_congestion = usage

            # --------------------------------------------------
            # FORCE NUMERIC FEATURES
            # --------------------------------------------------

            features = [[

                float(usage),

                float(road_length),

                float(speed_limit),

                float(nearby_congestion),

                float(road_type_encoded)
            ]]

            # --------------------------------------------------
            # Neural Network Weighting
            # --------------------------------------------------

            if use_neural_network:

                try:

                    prediction = float(

                        predict_congestion(
                            features
                        )
                    )

                    multiplier = (

                        1.0 +

                        prediction
                    )

                    multiplier = max(
                        1.0,
                        min(multiplier, 5.0)
                    )

                except Exception as error:

                    print(
                        f"Prediction error: {error}"
                    )

                    multiplier = 1.0

            # --------------------------------------------------
            # Smooth Static Weighting
            # --------------------------------------------------

            else:

                congestion_factor = (

                    usage /

                    max(average_edge_usage, 1)

                )

                multiplier = (

                        1.0 +

                        (congestion_factor ** 1.3) * 0.8
                )

                multiplier = min(
                    multiplier,
                    5.0
                )

            # --------------------------------------------------
            # UPDATED TRAVEL TIME
            # --------------------------------------------------

            updated_travel_time = (
                base_travel_time * multiplier
            )

            # --------------------------------------------------
            # CONGESTION MEMORY / DECAY
            # --------------------------------------------------

            updated_travel_time = (

                base_travel_time +

                (
                    updated_travel_time -

                    base_travel_time
                ) * 0.95
            )

            data["travel_time"] = (
                updated_travel_time
            )


# ==========================================================
# EXPORT RESULTS CSV
# ==========================================================

def export_results_csv(results):
    """
    Export simulation results.
    """

    file_exists = RESULTS_CSV_PATH.exists()

    with open(

        RESULTS_CSV_PATH,

        "a",

        newline=""
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([

                "vehicles",

                "algorithm",

                "weighting_mode",

                "rerouting",

                "average_edge_usage",

                "max_edge_usage",

                "total_travel_cost",

                "average_travel_cost",

                "green_edges",

                "yellow_edges",

                "orange_edges",

                "red_edges",

                "rerouted_vehicles",

                "runtime_seconds",

                "total_nodes_visited"
            ])

        writer.writerow(results)


# ==========================================================
# EXPORT TRAINING DATA
# ==========================================================

def export_training_data(
    graph,
    edge_usage
):
    """
    Export neural network
    training samples using
    observed congestion ratios.
    """

    file_exists = TRAINING_DATA_PATH.exists()

    with open(

        TRAINING_DATA_PATH,

        "a",

        newline=""
    ) as file:

        writer = csv.writer(file)

        # --------------------------------------------------
        # CSV HEADER
        # --------------------------------------------------

        if not file_exists:

            writer.writerow([

                "edge_usage",

                "road_length",

                "speed_limit",

                "nearby_congestion",

                "road_type",

                "congestion_ratio"
            ])

        # --------------------------------------------------
        # EDGE DATA EXPORT
        # --------------------------------------------------

        for u, v, key, data in graph.edges(

            keys=True,

            data=True
        ):

            usage = edge_usage.get(
                (u, v),
                0
            )

            road_length = data.get(
                "length",
                0
            )

            speed_limit = data.get(
                "speed_kph",
                30
            )

            if isinstance(speed_limit, list):

                speed_limit = speed_limit[0]

            road_type = data.get(
                "highway",
                "residential"
            )

            if isinstance(road_type, list):

                road_type = road_type[0]

            road_type_encoded = (
                ROAD_TYPE_MAPPING.get(
                    road_type,
                    5
                )
            )

            nearby_congestion = usage

            # --------------------------------------------------
            # OBSERVED CONGESTION
            # --------------------------------------------------

            base_travel_time = data.get(
                "base_travel_time",
                1
            )

            current_travel_time = data.get(
                "travel_time",
                base_travel_time
            )

            if base_travel_time == 0:

                base_travel_time = 1

            congestion_ratio = (

                current_travel_time /

                base_travel_time
            )

            # --------------------------------------------------
            # WRITE TRAINING SAMPLE
            # --------------------------------------------------

            writer.writerow([

                float(usage),

                float(road_length),

                float(speed_limit),

                float(nearby_congestion),

                float(road_type_encoded),

                float(congestion_ratio)
            ])