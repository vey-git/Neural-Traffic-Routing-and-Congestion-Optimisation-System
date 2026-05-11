import networkx as nx
import matplotlib.pyplot as mpl
import osmnx as os
import random

from numpy.ma.extras import average

from src.vehicle import Vehicle


# =========================
# USER INPUTS
# =========================

num_of_vehicles = int(
    input("How many vehicles do you want to simulate?: ")
)


# =========================
# GRAPH + ROUTING
# =========================

def runSimulation():

    # =========================
    # CREATE MASTER GRAPH
    # =========================

    G = os.graph_from_place(
        "Oxford, England",
        network_type="drive"
    )

    # add speed/travel time data
    G = os.add_edge_speeds(G)
    G = os.add_edge_travel_times(G)

    # all graph nodes
    Nodes = list(G.nodes)

    # =========================
    # GENERATE VEHICLES
    # =========================

    vehicles = []

    for i in range(0, num_of_vehicles):

        valid_route = False

        while not valid_route:

            # random start and goal nodes
            random_start = random.choice(Nodes)
            random_goal = random.choice(Nodes)

            # make sure start != goal
            while random_start == random_goal:
                random_goal = random.choice(Nodes)

            try:

                # create vehicle
                vehicle = Vehicle(
                    G,
                    random_start,
                    random_goal
                )

                # store vehicle
                vehicles.append(vehicle)

                # calculate number of vehicles that occupy a singular edge

                edge_count = {}

                for vehicle in vehicles:
                    route = vehicle.route
                    #iterate through neighbouring nodes to obtain edges
                    for i in range(len(route) - 1):
                        edge = (route[1], route[i+1])
                        if edge not in edge_count:
                            edge_count[edge] = 0
                        edge_count[edge] +=1

                #calculate edge average
                total = 0
                for edges in edge_count:
                    total += edge_count[edges]
                average_edge_count = total/len(edge_count)
                #calculate traffic per edge
                for edge in edge_count:

                    usage = edge_count[edge]

                    u, v = edge

                    # check edge exists in graph
                    if G.has_edge(u, v):
                        edge_data = G[u][v]

                        # get first available edge key
                        first_key = list(edge_data.keys())[0]

                        # current travel time
                        current_time = edge_data[first_key]['travel_time']

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

                        # update travel time
                        new_time = current_time * multiplier

                        edge_data[first_key]['travel_time'] = new_time


                # console output
                print(f"Vehicle {i + 1}")
                print("Start Node:", vehicle.start_node)
                print("Goal Node:", vehicle.goal_node)
                print("Current Node:", vehicle.current_node)
                print("Route Length:", len(vehicle.route))
                print()

                # route successfully created
                valid_route = True

            except nx.NetworkXNoPath:

                print("No valid path found. Generating new nodes...")

    # =========================
    # VISUALISATION
    # =========================

    edge_colours = []
    edge_widths = []

    # loop through all graph edges
    for u, v, key in G.edges(keys=True):

        usage = 0

        # check if edge exists in congestion dictionary
        if (u, v) in edge_count:
            usage = edge_count[(u, v)]

        # colour roads based on congestion
        if usage < average_edge_count * 0.5:

            edge_colours.append("lime")
            edge_widths.append(0.5)

        elif usage < average_edge_count:

            edge_colours.append("yellow")
            edge_widths.append(1)

        elif usage < average_edge_count * 1.5:

            edge_colours.append("orange")
            edge_widths.append(2)

        else:

            edge_colours.append("red")
            edge_widths.append(3)

    # plot graph
    fig, ax = os.plot_graph(
        G,
        node_size=0,
        edge_color=edge_colours,
        edge_linewidth=edge_widths,
        bgcolor='black',
        show=False,
        close=False
    )

    # title
    ax.set_title(
        "Oxford Traffic Congestion Simulation",
        fontsize=18,
        color='white',
        pad=20
    )

    # =========================
    # PLOT VEHICLES
    # =========================

    for vehicle in vehicles:
        ax.scatter(
            G.nodes[vehicle.current_node]['x'],
            G.nodes[vehicle.current_node]['y'],
            color='cyan',
            s=15,
            zorder=10
        )

    # =========================
    # SHOW PLOT
    # =========================

    mpl.show()

# =========================
# RUN PROGRAM
# =========================

runSimulation()
