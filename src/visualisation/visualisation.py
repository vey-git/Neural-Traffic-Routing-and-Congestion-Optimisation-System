import matplotlib.pyplot as mpl
import osmnx as os
import pandas as pd

from matplotlib.lines import Line2D

from utils.config import (
    PLOTS_DIR,
    RESULTS_CSV_PATH,
    FIGURE_DPI,
    HEATMAP_BACKGROUND,
    LOW_CONGESTION_COLOUR,
    MODERATE_CONGESTION_COLOUR,
    HIGH_CONGESTION_COLOUR,
    SEVERE_CONGESTION_COLOUR
)


# ======================================================
# GLOBAL STYLING
# ======================================================

mpl.style.use("ggplot")

TITLE_SIZE = 20
LABEL_SIZE = 14
TICK_SIZE = 12

LINE_WIDTH = 3
MARKER_SIZE = 8


# ======================================================
# HELPER FUNCTION
# ======================================================

def create_plot_path(
    category,
    filename
):
    """
    Create organised plot directories.
    """

    category_dir = (
        PLOTS_DIR / category
    )

    category_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return category_dir / filename


# ======================================================
# CONGESTION HEATMAP
# ======================================================

def plot_congestion_heatmap(

    graph,
    edge_usage,
    average_edge_usage,
    algorithm,
    vehicle_count,
    vehicles

):
    """
    Plot traffic congestion heatmap.
    """

    edge_colours = []
    edge_widths = []

    # --------------------------------------------------
    # Edge Colouring
    # --------------------------------------------------

    for u, v, key in graph.edges(keys=True):

        usage = edge_usage.get((u, v), 0)

        # LOW CONGESTION
        if usage < average_edge_usage * 0.5:

            edge_colours.append(
                LOW_CONGESTION_COLOUR
            )

            edge_widths.append(0.3)

        # MODERATE CONGESTION
        elif usage < average_edge_usage:

            edge_colours.append(
                MODERATE_CONGESTION_COLOUR
            )

            edge_widths.append(1)

        # HIGH CONGESTION
        elif usage < average_edge_usage * 1.5:

            edge_colours.append(
                HIGH_CONGESTION_COLOUR
            )

            edge_widths.append(2)

        # SEVERE CONGESTION
        else:

            edge_colours.append(
                SEVERE_CONGESTION_COLOUR
            )

            edge_widths.append(3)

    # --------------------------------------------------
    # Plot Graph
    # --------------------------------------------------

    fig, ax = os.plot_graph(

        graph,

        node_size=0,

        edge_color=edge_colours,

        edge_linewidth=edge_widths,

        bgcolor=HEATMAP_BACKGROUND,

        show=False,

        close=False

    )

    # --------------------------------------------------
    # Plot Vehicle Positions
    # --------------------------------------------------

    for vehicle in vehicles:

        ax.scatter(

            graph.nodes[
                vehicle.current_node
            ]["x"],

            graph.nodes[
                vehicle.current_node
            ]["y"],

            color="cyan",

            s=8,

            zorder=10

        )

    # --------------------------------------------------
    # Title
    # --------------------------------------------------

    ax.set_title(

        (
            f"{algorithm.upper()} "
            f"Traffic Heatmap "
            f"({vehicle_count} Vehicles)"
        ),

        fontsize=18,

        color="white",

        pad=20

    )

    # --------------------------------------------------
    # Legend
    # --------------------------------------------------

    legend_elements = [

        Line2D(
            [0],
            [0],
            color=LOW_CONGESTION_COLOUR,
            lw=4,
            label="Low Congestion"
        ),

        Line2D(
            [0],
            [0],
            color=MODERATE_CONGESTION_COLOUR,
            lw=4,
            label="Moderate Congestion"
        ),

        Line2D(
            [0],
            [0],
            color=HIGH_CONGESTION_COLOUR,
            lw=4,
            label="High Congestion"
        ),

        Line2D(
            [0],
            [0],
            color=SEVERE_CONGESTION_COLOUR,
            lw=4,
            label="Severe Congestion"
        )

    ]

    ax.legend(

        handles=legend_elements,

        loc="lower left",

        fontsize=10

    )

    # --------------------------------------------------
    # Save Figure
    # --------------------------------------------------

    save_path = create_plot_path(

        "heatmaps",

        (
            f"heatmap_"
            f"{algorithm}_"
            f"{vehicle_count}.png"
        )

    )

    mpl.savefig(

        save_path,

        dpi=FIGURE_DPI,

        bbox_inches="tight"

    )

    mpl.close()


# ======================================================
# RESULTS VISUALISATION
# ======================================================

def plot_results_graphs():
    """
    Generate simulation comparison graphs.
    """

    data = pd.read_csv(
        RESULTS_CSV_PATH
    )

    # remove accidental spaces
    data["algorithm"] = (
        data["algorithm"].str.strip()
    )

    # split algorithms
    dijkstra_data = data[
        data["algorithm"] == "dijkstra"
    ]

    astar_data = data[
        data["algorithm"] == "astar"
    ]

    # --------------------------------------------------
    # Graph Definitions
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Generate Graphs
    # --------------------------------------------------

    for metric, title, ylabel, filename in graphs:

        fig, ax = mpl.subplots(
            figsize=(11, 6)
        )

        ax.plot(

            dijkstra_data["vehicles"],
            dijkstra_data[metric],

            marker="o",

            linewidth=LINE_WIDTH,

            markersize=MARKER_SIZE,

            label="Dijkstra"

        )

        ax.plot(

            astar_data["vehicles"],
            astar_data[metric],

            marker="o",

            linewidth=LINE_WIDTH,

            markersize=MARKER_SIZE,

            label="A*"

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

        save_path = create_plot_path(
            "results",
            filename
        )

        mpl.savefig(

            save_path,

            dpi=FIGURE_DPI,

            bbox_inches="tight"

        )

        mpl.close()

    # --------------------------------------------------
    # Logarithmic Runtime Graph
    # --------------------------------------------------

    fig, ax = mpl.subplots(
        figsize=(11, 6)
    )

    ax.plot(

        dijkstra_data["vehicles"],
        dijkstra_data["runtime_seconds"],

        marker="o",

        linewidth=LINE_WIDTH,

        markersize=MARKER_SIZE,

        label="Dijkstra"

    )

    ax.plot(

        astar_data["vehicles"],
        astar_data["runtime_seconds"],

        marker="o",

        linewidth=LINE_WIDTH,

        markersize=MARKER_SIZE,

        label="A*"

    )

    ax.set_xscale("log")

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

    save_path = create_plot_path(

        "results",

        "logarithmic_runtime_scaling.png"

    )

    mpl.savefig(

        save_path,

        dpi=FIGURE_DPI,

        bbox_inches="tight"

    )

    mpl.close()

    print(
        "\n===== VISUALISATION COMPLETE ====="
    )


# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    plot_results_graphs()