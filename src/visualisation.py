import pandas as pd
import matplotlib.pyplot as mpl


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
# LOAD CSV DATA
# =========================

# results.csv should be generated
# automatically from metrics.py

data = pd.read_csv("results.csv")


# =========================
# GRAPH 1
# RUNTIME SCALING
# =========================

fig, ax = mpl.subplots(figsize=(11, 6))

ax.plot(
    data["vehicles"],
    data["runtime_seconds"],
    marker='o',
    linewidth=LINE_WIDTH,
    markersize=MARKER_SIZE,
    label='Runtime'
)

ax.set_title(
    "Simulation Runtime Scaling",
    fontsize=TITLE_SIZE,
    pad=15
)

ax.set_xlabel(
    "Number of Vehicles",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "Runtime (seconds)",
    fontsize=LABEL_SIZE
)

ax.tick_params(labelsize=TICK_SIZE)

ax.grid(True)

ax.legend(fontsize=12)

mpl.tight_layout()

mpl.savefig(
    "runtime_scaling.png",
    dpi=300
)

mpl.show()


# =========================
# GRAPH 2
# AVERAGE EDGE USAGE
# =========================

fig, ax = mpl.subplots(figsize=(11, 6))

ax.plot(
    data["vehicles"],
    data["average_edge_usage"],
    marker='o',
    linewidth=LINE_WIDTH,
    markersize=MARKER_SIZE,
    label='Average Edge Usage'
)

ax.set_title(
    "Average Congestion Growth",
    fontsize=TITLE_SIZE,
    pad=15
)

ax.set_xlabel(
    "Number of Vehicles",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "Average Edge Usage",
    fontsize=LABEL_SIZE
)

ax.tick_params(labelsize=TICK_SIZE)

ax.grid(True)

ax.legend(fontsize=12)

mpl.tight_layout()

mpl.savefig(
    "average_congestion_growth.png",
    dpi=300
)

mpl.show()


# =========================
# GRAPH 3
# MAXIMUM BOTTLENECK
# =========================

fig, ax = mpl.subplots(figsize=(11, 6))

ax.plot(
    data["vehicles"],
    data["max_edge_usage"],
    marker='o',
    linewidth=LINE_WIDTH,
    markersize=MARKER_SIZE,
    label='Maximum Edge Usage'
)

ax.set_title(
    "Maximum Bottleneck Severity",
    fontsize=TITLE_SIZE,
    pad=15
)

ax.set_xlabel(
    "Number of Vehicles",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "Maximum Edge Usage",
    fontsize=LABEL_SIZE
)

ax.tick_params(labelsize=TICK_SIZE)

ax.grid(True)

ax.legend(fontsize=12)

mpl.tight_layout()

mpl.savefig(
    "maximum_bottleneck_severity.png",
    dpi=300
)

mpl.show()


# =========================
# GRAPH 4
# ADAPTIVE REROUTING
# =========================

fig, ax = mpl.subplots(figsize=(11, 6))

ax.plot(
    data["vehicles"],
    data["rerouted_vehicles"],
    marker='o',
    linewidth=LINE_WIDTH,
    markersize=MARKER_SIZE,
    label='Rerouted Vehicles'
)

ax.set_title(
    "Adaptive Rerouting Behaviour",
    fontsize=TITLE_SIZE,
    pad=15
)

ax.set_xlabel(
    "Number of Vehicles",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "Vehicles Rerouted",
    fontsize=LABEL_SIZE
)

ax.tick_params(labelsize=TICK_SIZE)

ax.grid(True)

ax.legend(fontsize=12)

mpl.tight_layout()

mpl.savefig(
    "adaptive_rerouting_behaviour.png",
    dpi=300
)

mpl.show()


# =========================
# GRAPH 5
# AVERAGE TRAVEL COST
# =========================

fig, ax = mpl.subplots(figsize=(11, 6))

ax.plot(
    data["vehicles"],
    data["average_travel_cost"],
    marker='o',
    linewidth=LINE_WIDTH,
    markersize=MARKER_SIZE,
    label='Average Travel Cost'
)

ax.set_title(
    "Average Vehicle Travel Cost",
    fontsize=TITLE_SIZE,
    pad=15
)

ax.set_xlabel(
    "Number of Vehicles",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "Average Travel Cost",
    fontsize=LABEL_SIZE
)

ax.tick_params(labelsize=TICK_SIZE)

ax.grid(True)

ax.legend(fontsize=12)

mpl.tight_layout()

mpl.savefig(
    "average_vehicle_travel_cost.png",
    dpi=300
)

mpl.show()


# =========================
# GRAPH 6
# TOTAL NETWORK COST
# =========================

fig, ax = mpl.subplots(figsize=(11, 6))

ax.plot(
    data["vehicles"],
    data["total_travel_cost"],
    marker='o',
    linewidth=LINE_WIDTH,
    markersize=MARKER_SIZE,
    label='Total Network Cost'
)

ax.set_title(
    "Total Network Travel Cost",
    fontsize=TITLE_SIZE,
    pad=15
)

ax.set_xlabel(
    "Number of Vehicles",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "Total Travel Cost",
    fontsize=LABEL_SIZE
)

ax.tick_params(labelsize=TICK_SIZE)

ax.grid(True)

ax.legend(fontsize=12)

mpl.tight_layout()

mpl.savefig(
    "total_network_travel_cost.png",
    dpi=300
)

mpl.show()


# =========================
# GRAPH 7
# CONGESTION DISTRIBUTION
# =========================

fig, ax = mpl.subplots(figsize=(12, 7))

bar_width = 0.2

x = range(len(data["vehicles"]))

ax.bar(
    [i - bar_width for i in x],
    data["green_edges"],
    width=bar_width,
    label='Low Congestion'
)

ax.bar(
    x,
    data["yellow_edges"],
    width=bar_width,
    label='Moderate Congestion'
)

ax.bar(
    [i + bar_width for i in x],
    data["red_edges"],
    width=bar_width,
    label='Heavy Congestion'
)

ax.set_title(
    "Congestion Distribution Across Vehicle Loads",
    fontsize=TITLE_SIZE,
    pad=15
)

ax.set_xlabel(
    "Simulation Run",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "Number of Edges",
    fontsize=LABEL_SIZE
)

ax.set_xticks(list(x))

ax.set_xticklabels(data["vehicles"])

ax.tick_params(labelsize=TICK_SIZE)

ax.legend(fontsize=12)

ax.grid(True)

mpl.tight_layout()

mpl.savefig(
    "congestion_distribution.png",
    dpi=300
)

mpl.show()


# =========================
# GRAPH 8
# LOGARITHMIC RUNTIME
# =========================

fig, ax = mpl.subplots(figsize=(11, 6))

ax.plot(
    data["vehicles"],
    data["runtime_seconds"],
    marker='o',
    linewidth=LINE_WIDTH,
    markersize=MARKER_SIZE
)

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

ax.tick_params(labelsize=TICK_SIZE)

ax.grid(True)

mpl.tight_layout()

mpl.savefig(
    "logarithmic_runtime_scaling.png",
    dpi=300
)

mpl.show()


# =========================
# FINAL SUMMARY
# =========================

print("\n===== VISUALISATION COMPLETE =====")
print("Saved all figures as high-quality PNG files.")