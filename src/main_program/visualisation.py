import matplotlib.pyplot as mpl
import osmnx as os
import pandas as pd


# =========================
# GLOBAL STYLING
# =========================

mpl.style.use('ggplot')

TITLE_SIZE = 20
LABEL_SIZE = 14
TICK_SIZE = 12

LINE_WIDTH = 3
MARKER_SIZE = 8


# =========================
# HEATMAP FUNCTION
# =========================

def plotCongestionHeatmap(

    G,
    edge_count,
    average_edge_usage,
    algorithm,
    vehicle_count,
    vehicles

):

    edge_colours = []
    edge_widths = []

    # =========================
    # EDGE COLOURS
    # =========================

    for u, v, key in G.edges(keys=True):

        usage = 0

        if (u, v) in edge_count:

            usage = edge_count[(u, v)]

        # LOW CONGESTION
        if usage < average_edge_usage * 0.5:

            edge_colours.append("lime")
            edge_widths.append(0.3)

        # MODERATE CONGESTION
        elif usage < average_edge_usage:

            edge_colours.append("yellow")
            edge_widths.append(1)

        # HIGH CONGESTION
        elif usage < average_edge_usage * 1.5:

            edge_colours.append("orange")
            edge_widths.append(2)

        # SEVERE CONGESTION
        else:

            edge_colours.append("red")
            edge_widths.append(3)

    # =========================
    # PLOT GRAPH
    # =========================

    fig, ax = os.plot_graph(

        G,

        node_size=0,

        edge_color=edge_colours,

        edge_linewidth=edge_widths,

        bgcolor='black',

        show=False,

        close=False

    )

    # =========================
    # PLOT VEHICLES
    # =========================

    for vehicle in vehicles:

        ax.scatter(

            G.nodes[vehicle.current_node]['x'],

            G.nodes[vehicle.current_node]['y'],

            color='cyan',

            s=8,

            zorder=10

        )

    # =========================
    # TITLE
    # =========================

    ax.set_title(

        f"{algorithm.upper()} Traffic Heatmap ({vehicle_count} Vehicles)",

        fontsize=18,

        color='white',

        pad=20

    )

    # =========================
    # SAVE IMAGE
    # =========================
    from matplotlib.lines import Line2D

    legend_elements = [

        Line2D(
            [0],
            [0],
            color='lime',
            lw=4,
            label='Low Congestion'
        ),

        Line2D(
            [0],
            [0],
            color='yellow',
            lw=4,
            label='Moderate Congestion'
        ),

        Line2D(
            [0],
            [0],
            color='orange',
            lw=4,
            label='High Congestion'
        ),

        Line2D(
            [0],
            [0],
            color='red',
            lw=4,
            label='Severe Congestion'
        )

    ]

    ax.legend(
        handles=legend_elements,
        loc='lower left',
        fontsize=10
    )
    mpl.savefig(

        f"heatmap_{algorithm}_{vehicle_count}.png",

        dpi=300,

        bbox_inches='tight'

    )

    mpl.show()


# =========================
# RESULTS GRAPH FUNCTION
# =========================

def plotResultsGraphs():

    data = pd.read_csv("results.csv")

    # remove accidental spaces
    data["algorithm"] = data["algorithm"].str.strip()

    # split algorithms
    dijkstra_data = data[
        data["algorithm"] == "dijkstra"
    ]

    astar_data = data[
        data["algorithm"] == "astar"
    ]

    # =========================
    # ALL STANDARD GRAPHS
    # =========================

    graphs = [

        (
            "runtime_seconds",
            "Runtime Scaling Comparison",
            "Runtime (seconds)",
            "runtime_comparison.png"
        ),

        (
            "average_edge_usage",
            "Average Congestion Comparison",
            "Average Edge Usage",
            "average_congestion_comparison.png"
        ),

        (
            "max_edge_usage",
            "Maximum Bottleneck Severity",
            "Maximum Edge Usage",
            "maximum_bottleneck_comparison.png"
        ),

        (
            "rerouted_vehicles",
            "Adaptive Rerouting Behaviour",
            "Vehicles Rerouted",
            "adaptive_rerouting_comparison.png"
        ),

        (
            "total_travel_cost",
            "Total Network Travel Cost",
            "Total Travel Cost",
            "total_travel_cost_comparison.png"
        )
    ]

    # =========================
    # GENERATE STANDARD GRAPHS
    # =========================

    for metric, title, ylabel, filename in graphs:

        fig, ax = mpl.subplots(figsize=(11, 6))

        ax.plot(

            dijkstra_data["vehicles"],
            dijkstra_data[metric],

            marker='o',
            linewidth=LINE_WIDTH,
            markersize=MARKER_SIZE,

            label='Dijkstra'

        )

        ax.plot(

            astar_data["vehicles"],
            astar_data[metric],

            marker='o',
            linewidth=LINE_WIDTH,
            markersize=MARKER_SIZE,

            label='A*'

        )

        ax.set_title(
            title,
            fontsize=TITLE_SIZE,
            pad=15
        )

        ax.set_xlabel(
            "Number of Vehicles",
            fontsize=LABEL_SIZE
        )

        ax.set_ylabel(
            ylabel,
            fontsize=LABEL_SIZE
        )

        ax.tick_params(
            labelsize=TICK_SIZE
        )

        ax.grid(True)

        ax.legend(fontsize=12)

        mpl.tight_layout()

        mpl.savefig(
            filename,
            dpi=300
        )

        mpl.show()

    # =========================
    # LOGARITHMIC RUNTIME GRAPH
    # =========================

    fig, ax = mpl.subplots(figsize=(11, 6))

    ax.plot(

        dijkstra_data["vehicles"],
        dijkstra_data["runtime_seconds"],

        marker='o',
        linewidth=LINE_WIDTH,
        markersize=MARKER_SIZE,

        label='Dijkstra'

    )

    ax.plot(

        astar_data["vehicles"],
        astar_data["runtime_seconds"],

        marker='o',
        linewidth=LINE_WIDTH,
        markersize=MARKER_SIZE,

        label='A*'

    )

    # logarithmic scale
    ax.set_xscale('log')

    ax.set_title(
        "Logarithmic Runtime Scaling",
        fontsize=TITLE_SIZE,
        pad=15
    )

    ax.set_xlabel(
        "Number of Vehicles (log scale)",
        fontsize=LABEL_SIZE
    )

    ax.set_ylabel(
        "Runtime (seconds)",
        fontsize=LABEL_SIZE
    )

    ax.tick_params(
        labelsize=TICK_SIZE
    )

    ax.grid(True)

    ax.legend(fontsize=12)

    mpl.tight_layout()

    mpl.savefig(
        "logarithmic_runtime_scaling.png",
        dpi=300
    )

    mpl.show()

    print("\n===== VISUALISATION COMPLETE =====")


# =========================
# RUN VISUALISATIONS
# =========================

if __name__ == "__main__":

    plotResultsGraphs()