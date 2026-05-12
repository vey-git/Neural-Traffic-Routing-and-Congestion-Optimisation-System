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



def calculateAverageEdgeUsage(edge_count):

    total = 0

    for edge in edge_count:

        total += edge_count[edge]

    average_edge_count = total / len(edge_count)

    return average_edge_count



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