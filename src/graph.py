import networkx as nx
import matplotlib.pyplot as mpl
import osmnx as os
import random

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

        # random start and goal nodes
        random_start = random.choice(Nodes)
        random_goal = random.choice(Nodes)

        # make sure start != goal
        while random_start == random_goal:
            random_goal = random.choice(Nodes)

        # create vehicle
        vehicle = Vehicle(
            G,
            random_start,
            random_goal
        )

        # store vehicle
        vehicles.append(vehicle)

        # console output
        print(f"Vehicle {i + 1}")
        print("Start Node:", vehicle.start_node)
        print("Goal Node:", vehicle.goal_node)
        print("Current Node:", vehicle.current_node)
        print("Route Length:", len(vehicle.route))
        print()

    # =========================
    # VISUALISATION
    # =========================

    fig, ax = os.plot_graph(
        G,
        node_size=0,
        edge_color='white',
        edge_linewidth=0.5,
        bgcolor='black',
        show=False,
        close=False
    )

    # title
    ax.set_title(
        "Traffic Routing Simulation",
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
            color='yellow',
            s=40,
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