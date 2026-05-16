import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# LOAD RESULTS
# ==========================================

df = pd.read_csv("results_nn.csv")

# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

df.columns = df.columns.str.strip()

# ==========================================
# REMOVE BROKEN ROWS
# ==========================================

df = df.dropna()

# ==========================================
# CREATE WEIGHTING MODE COLUMN
# IF IT DOES NOT EXIST
# ==========================================

if "weighting_mode" not in df.columns:

    df["weighting_mode"] = "static"

    df.loc[

        df["algorithm"].astype(str).str.contains(

            "neural",

            case=False,

            na=False

        ),

        "weighting_mode"

    ] = "neural_network"

# ==========================================
# CLEAN ALGORITHM NAMES
# ==========================================

df["algorithm"] = df["algorithm"].replace({

    "astar_neural": "astar",

    "dijkstra_neural": "dijkstra"

})

# ==========================================
# FIX RUNTIME COLUMN
# ==========================================

if "runtime_seconds" not in df.columns:

    if "runtime" in df.columns:

        df["runtime_seconds"] = df["runtime"]

# ==========================================
# NUMERIC COLUMNS
# ==========================================

numeric_columns = [

    "vehicles",

    "average_edge_usage",

    "max_edge_usage",

    "total_travel_cost",

    "average_travel_cost",

    "rerouted_vehicles",

    "runtime_seconds",

    "total_nodes_visited"

]

# ==========================================
# CONVERT TO NUMERIC
# ==========================================

for col in numeric_columns:

    df[col] = pd.to_numeric(

        df[col],

        errors="coerce"

    )

# ==========================================
# REMOVE INVALID ROWS
# ==========================================

df = df.dropna()

# ==========================================
# GROUP + CALCULATE AVERAGES
# ==========================================

average_results = df.groupby(

    [

        "vehicles",

        "algorithm",

        "weighting_mode"

    ]

).mean(

    numeric_only=True

).reset_index()

# ==========================================
# SAVE AVERAGES
# ==========================================

average_results.to_csv(

    "average_results.csv",

    index=False

)

print("\n===== AVERAGED RESULTS =====\n")

print(average_results)

# ==========================================
# GENERIC GRAPH FUNCTION
# ==========================================

def createGraph(

    y_column,

    title,

    ylabel,

    filename

):

    plt.figure(figsize=(10, 6))

    for (algorithm, weighting), group in average_results.groupby(

        [

            "algorithm",

            "weighting_mode"

        ]

    ):

        label = f"{algorithm} - {weighting}"

        plt.plot(

            group["vehicles"],

            group[y_column],

            marker='o',

            linewidth=2,

            label=label

        )

    plt.title(title)

    plt.xlabel("Number of Vehicles")

    plt.ylabel(ylabel)

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()

# ==========================================
# GRAPH 1
# AVERAGE TRAVEL COST
# ==========================================

createGraph(

    "average_travel_cost",

    "Average Travel Cost vs Vehicles",

    "Average Travel Cost",

    "graph_average_travel_cost.png"

)

# ==========================================
# GRAPH 2
# AVERAGE EDGE USAGE
# ==========================================

createGraph(

    "average_edge_usage",

    "Average Edge Usage vs Vehicles",

    "Average Edge Usage",

    "graph_average_edge_usage.png"

)

# ==========================================
# GRAPH 3
# MAX EDGE USAGE
# ==========================================

createGraph(

    "max_edge_usage",

    "Maximum Edge Usage vs Vehicles",

    "Maximum Edge Usage",

    "graph_max_edge_usage.png"

)

# ==========================================
# GRAPH 4
# RUNTIME
# ==========================================

createGraph(

    "runtime_seconds",

    "Runtime Scalability vs Vehicles",

    "Runtime (seconds)",

    "graph_runtime.png"

)

# ==========================================
# GRAPH 5
# REROUTED VEHICLES
# ==========================================

createGraph(

    "rerouted_vehicles",

    "Rerouted Vehicles vs Vehicles",

    "Rerouted Vehicles",

    "graph_rerouted_vehicles.png"

)

# ==========================================
# GRAPH 6
# NODES VISITED
# ==========================================

createGraph(

    "total_nodes_visited",

    "Average Nodes Visited vs Vehicles",

    "Average Nodes Visited",

    "graph_nodes_visited.png"

)

# =========================================================
# LOAD AVERAGED RESULTS
# =========================================================

df = pd.read_csv("average_results.csv")

# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = df.columns.str.strip()

# =========================================================
# OPTIONAL:
# MAKE LABELS LOOK CLEANER
# =========================================================

df["method"] = (
    df["algorithm"].str.upper()
    + " - "
    + df["weighting_mode"].str.replace("_", " ").str.title()
)

# =========================================================
# GLOBAL GRAPH STYLE
# =========================================================

plt.style.use("seaborn-v0_8-whitegrid")

FONT_SIZE = 13
TITLE_SIZE = 16

# =========================================================
# HELPER FUNCTION
# =========================================================

def create_graph(
    y_column,
    y_label,
    title,
    filename
):

    plt.figure(figsize=(10, 6))

    for method in df["method"].unique():

        subset = df[df["method"] == method]

        plt.plot(
            subset["vehicles"],
            subset[y_column],
            marker='o',
            linewidth=2.5,
            markersize=7,
            label=method
        )

    plt.xlabel(
        "Number of Vehicles",
        fontsize=FONT_SIZE
    )

    plt.ylabel(
        y_label,
        fontsize=FONT_SIZE
    )

    plt.title(
        title,
        fontsize=TITLE_SIZE,
        fontweight='bold'
    )

    plt.legend(
        fontsize=11
    )

    plt.xticks(
        fontsize=11
    )

    plt.yticks(
        fontsize=11
    )

    plt.tight_layout()

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches='tight'
    )

    plt.show()

# =========================================================
# GRAPH 1
# AVERAGE TRAVEL COST
# =========================================================

create_graph(

    y_column="average_travel_cost",

    y_label="Average Travel Cost",

    title="Average Travel Cost vs Vehicle Count",

    filename="average_travel_cost.png"

)

# =========================================================
# GRAPH 2
# RUNTIME
# =========================================================

create_graph(

    y_column="runtime_seconds",

    y_label="Runtime (Seconds)",

    title="Runtime Scalability Comparison",

    filename="runtime_scalability.png"

)

# =========================================================
# GRAPH 3
# AVERAGE EDGE USAGE
# =========================================================

create_graph(

    y_column="average_edge_usage",

    y_label="Average Edge Usage",

    title="Average Edge Usage vs Vehicle Count",

    filename="average_edge_usage.png"

)

# =========================================================
# GRAPH 4
# MAXIMUM EDGE USAGE
# =========================================================

create_graph(

    y_column="max_edge_usage",

    y_label="Maximum Edge Usage",

    title="Maximum Congestion Bottleneck Comparison",

    filename="max_edge_usage.png"

)

# =========================================================
# GRAPH 5
# REROUTED VEHICLES
# =========================================================

create_graph(

    y_column="rerouted_vehicles",

    y_label="Vehicles Rerouted",

    title="Adaptive Rerouting Behaviour",

    filename="rerouted_vehicles.png"

)

# =========================================================
# GRAPH 6
# NODES VISITED
# =========================================================

create_graph(

    y_column="total_nodes_visited",

    y_label="Average Nodes Explored",

    title="Search Space Exploration Comparison",

    filename="nodes_visited.png"

)

print("\nGraphs generated successfully.")

print("\nGraphs generated successfully.")