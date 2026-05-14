import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# LOAD CSV
# ==========================================

df = pd.read_csv("results.csv")

# ==========================================
# CLEAN DATA
# ==========================================

# remove broken rows
df = df.dropna()

# convert numeric columns
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

for col in numeric_columns:

    df[col] = pd.to_numeric(df[col])

# ==========================================
# GROUP + AVERAGE RESULTS
# ==========================================

grouped = df.groupby(

    ["vehicles", "algorithm"]

).mean(numeric_only=True).reset_index()

# ==========================================
# SPLIT ALGORITHMS
# ==========================================

astar = grouped[grouped["algorithm"] == "astar"]

dijkstra = grouped[grouped["algorithm"] == "dijkstra"]

# ==========================================
# GRAPH 1
# RUNTIME SCALABILITY
# ==========================================

plt.figure(figsize=(8,6))

plt.plot(
    astar["vehicles"],
    astar["runtime_seconds"],
    marker='o',
    label="A*"
)

plt.plot(
    dijkstra["vehicles"],
    dijkstra["runtime_seconds"],
    marker='o',
    label="Dijkstra"
)

plt.xlabel("Number of Vehicles")
plt.ylabel("Runtime (seconds)")

plt.title("Runtime Scalability Comparison")

plt.legend()

plt.grid(True)

plt.savefig("runtime_scalability.png")

plt.show()

# ==========================================
# GRAPH 2
# MAX BOTTLENECK
# ==========================================

plt.figure(figsize=(8,6))

plt.plot(
    astar["vehicles"],
    astar["max_edge_usage"],
    marker='o',
    label="A*"
)

plt.plot(
    dijkstra["vehicles"],
    dijkstra["max_edge_usage"],
    marker='o',
    label="Dijkstra"
)

plt.xlabel("Number of Vehicles")
plt.ylabel("Maximum Edge Usage")

plt.title("Maximum Bottleneck Severity")

plt.legend()

plt.grid(True)

plt.savefig("max_bottleneck.png")

plt.show()

# ==========================================
# GRAPH 3
# AVERAGE TRAVEL COST
# ==========================================

plt.figure(figsize=(8,6))

plt.plot(
    astar["vehicles"],
    astar["average_travel_cost"],
    marker='o',
    label="A*"
)

plt.plot(
    dijkstra["vehicles"],
    dijkstra["average_travel_cost"],
    marker='o',
    label="Dijkstra"
)

plt.xlabel("Number of Vehicles")
plt.ylabel("Average Travel Cost")

plt.title("Average Travel Cost Comparison")

plt.legend()

plt.grid(True)

plt.savefig("average_travel_cost.png")

plt.show()

# ==========================================
# GRAPH 4
# REROUTED VEHICLES
# ==========================================

plt.figure(figsize=(8,6))

plt.plot(
    astar["vehicles"],
    astar["rerouted_vehicles"],
    marker='o',
    label="A*"
)

plt.plot(
    dijkstra["vehicles"],
    dijkstra["rerouted_vehicles"],
    marker='o',
    label="Dijkstra"
)

plt.xlabel("Number of Vehicles")
plt.ylabel("Rerouted Vehicles")

plt.title("Adaptive Rerouting Behaviour")

plt.legend()

plt.grid(True)

plt.savefig("rerouted_vehicles.png")

plt.show()

# ==========================================
# GRAPH 5
# AVERAGE NODES VISITED
# ==========================================

plt.figure(figsize=(8,6))

plt.plot(
    astar["vehicles"],
    astar["total_nodes_visited"],
    marker='o',
    label="A*"
)

plt.plot(
    dijkstra["vehicles"],
    dijkstra["total_nodes_visited"],
    marker='o',
    label="Dijkstra"
)

plt.xlabel("Number of Vehicles")
plt.ylabel("Average Route Nodes")

plt.title("Average Nodes Visited Comparison")

plt.legend()

plt.grid(True)

plt.savefig("nodes_visited.png")

plt.show()

# ==========================================
# EXPORT AVERAGED RESULTS
# ==========================================

grouped.to_csv(

    "averaged_results.csv",

    index=False

)

print("\nGraphs generated successfully.")