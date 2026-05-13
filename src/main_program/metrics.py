import csv
import networkx as nx


# =========================
# EDGE USAGE
# =========================

def calculateEdgeUsage(vehicles):

    edge_count = {}

    for vehicle in vehicles:

        route = vehicle.route

        for i in range(len(route) - 1):

            edge = (route[i], route[i + 1])

            if edge not in edge_count:
                edge_count[edge] = 0

            edge_count[edge] += 1

    return edge_count


# =========================
# AVERAGE EDGE USAGE
# =========================

def calculateAverageEdgeUsage(edge_count):

    total = 0

    for edge in edge_count:

        total += edge_count[edge]

    average_edge_count = total / len(edge_count)

    return average_edge_count


# =========================
# MAX EDGE USAGE
# =========================

def calculateMaxEdgeUsage(edge_count):

    max_usage = max(edge_count.values())

    return max_usage


# =========================
# TOTAL TRAVEL COST
# =========================

def calculateTotalTravelCost(G, vehicles):

    total_cost = 0

    for vehicle in vehicles:

        route_cost = nx.path_weight(
            G,
            vehicle.route,
            weight='travel_time'
        )

        total_cost += route_cost

    return total_cost


# =========================
# AVERAGE TRAVEL COST
# =========================

def calculateAverageTravelCost(G, vehicles):

    total_cost = calculateTotalTravelCost(G, vehicles)

    average_cost = total_cost / len(vehicles)

    return average_cost


# =========================
# CONGESTION DISTRIBUTION
# =========================

def countCongestionLevels(edge_count, average_edge_count):

    green = 0
    yellow = 0
    orange = 0
    red = 0

    for edge in edge_count:

        usage = edge_count[edge]

        if usage < average_edge_count * 0.5:

            green += 1

        elif usage < average_edge_count:

            yellow += 1

        elif usage < average_edge_count * 1.5:

            orange += 1

        else:

            red += 1

    return {
        "green": green,
        "yellow": yellow,
        "orange": orange,
        "red": red
    }


# =========================
# ROUTE CHANGE COUNT
# =========================

def calculateRouteChanges(vehicles):

    changed_routes = 0

    for vehicle in vehicles:

        if vehicle.original_route != vehicle.route:

            changed_routes += 1

    return changed_routes


# =========================
# CONGESTION WEIGHTING
# =========================

def updateCongestionWeights(G, edge_count, average_edge_count):

    for edge in edge_count:

        usage = edge_count[edge]

        u, v = edge

        if G.has_edge(u, v):

            edge_data = G[u][v]

            # IMPORTANT
            # update ALL parallel edges
            for key in edge_data:

                base_time = edge_data[key]['base_travel_time']

                # congestion multiplier
                if usage < average_edge_count * 0.5:

                    multiplier = 1.0

                elif usage < average_edge_count:

                    multiplier = 1.1

                elif usage < average_edge_count * 1.5:

                    multiplier = 1.4

                elif usage < average_edge_count * 2:

                    multiplier = 1.8

                else:

                    multiplier = 2.5

                new_time = base_time * multiplier

                edge_data[key]['travel_time'] = new_time


# =========================
# EXPORT RESULTS
# =========================

def exportResultsCSV(results):

    file_exists = False

    try:
        open("results.csv", "r")
        file_exists = True

    except FileNotFoundError:
        pass

    with open("results.csv", "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "vehicles",
                "algorithm",
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
                "runtime_seconds"
            ])

        writer.writerow(results)

def exportTrainingData(

                G,

                edge_count,

                average_edge_usage

        ):

            with open("../artificial_intelligence/training_data.csv", "a", newline="") as file:

                writer = csv.writer(file)

                for u, v, key, data in G.edges(keys=True, data=True):

                    usage = edge_count.get((u, v), 0)

                    road_length = data.get("length", 0)
                    speed_limit = data.get("speed_kph", 30)

                    if isinstance(speed_limit, list):
                        speed_limit = speed_limit[0]

                    road_type = data.get("highway", "residential")

                    if isinstance(road_type, list):
                        road_type = road_type[0]

                    road_mapping = {

                        "motorway": 0,

                        "trunk": 1,

                        "primary": 2,

                        "secondary": 3,

                        "tertiary": 4,

                        "residential": 5

                    }

                    road_type_encoded = road_mapping.get(

                        road_type,

                        5

                    )

                    if usage < average_edge_usage * 0.5:

                        multiplier = 1.0

                    elif usage < average_edge_usage:

                        multiplier = 1.5

                    elif usage < average_edge_usage * 1.5:

                        multiplier = 2.0

                    else:

                        multiplier = 3.0


                    nearby_congestion = usage

                    writer.writerow([

                        usage,

                        road_length,

                        speed_limit,

                        nearby_congestion,

                        road_type_encoded,

                        multiplier

                    ])