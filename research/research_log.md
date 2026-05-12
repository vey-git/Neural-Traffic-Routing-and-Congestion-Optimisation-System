research notes:

mathematical background of the strongest classical representation of routing and pathfinding is Dijkstras algorithm "A* has become a common option for researchers attempting to solve pathfinding problems" --> Foead, D., Ghifari, A., Kusuma, M.B., Hanafiah, N. and Gunawan, E. (2021). A Systematic Literature Review of A* Pathfinding. Procedia Computer Science, 179, pp.507–514. doi:https://doi.org/10.1016/j.procs.2021.01.034.
‌ 
Math representation is 𝑓(𝑛)=𝑔(𝑛)+ℎ(𝑛) where g(n) is the cost from the start node to "n", where h(n) is the estimated cost from "n" to the goal.

To generate our initial weighted graph we will use "networkx"  - Kapanowski, A. and Gałuszka, Ł. (2015). Weighted graph algorithms with Python. [online] arXiv.org. doi:https://doi.org/10.48550/arXiv.1504.07828.
‌
This has a simple way to generate graphs and can also be used in conjunction with osmnx

ran into issues with the following error: ValueError: Found no graph nodes within the requested polygon.
where a location of coordinates werent working within the algorithm. -> fixed by increasing the dist value 

need to calculate the distance between the 2 points, using as the euclidean distance which can be obtained by the osmnx library "great circle" 
we the needed to be able to obtain the users "string" inputs and turn them into coordinates for more accuracy which was done with geocoding -> https://www.geeksforgeeks.org/python/how-to-get-geolocation-in-python/

succesfully was able to generate a route from position a to position b.

Research goal -> traffic conditions
:there are multiple ways to measure congestion : basic, ratio, level of service and indices. Where these are based of delay estimation: a formula for determining congestion times is D ×
s V
= (1)
[ ] p
TT
−
TT
ac
ap
/
D ×
s V
=
Where, Ds = segment delay (vehicle-minutes)
D/
s = segment delay (person-minutes)
TTac = actual travel time (minutes)
TTap = acceptable travel time (minutes)
Vp = vehicle volume in the peak-period (vehicles)
Voc = vehicle occupancy (persons/vehicle) --> Aftabuzzaman, M. (2007). Measuring Traffic Congestion-A Critical Review. [online] Available at: https://australasiantransportresearchforum.org.au/wp-content/uploads/2022/03/2007_Aftabuzzaman.pdf.
‌

Ways of mitigating congestion: as total number of cars on a road exceeds maximum value which has been determines, that routes weight is altered to reflect it being slower. this would impact route changes efficiently by determining whether the overall time on that road will be quicker than rerouting onto a different road with less drivers. "Our starting point is a road network and an Origin-Destination (OD) matrix specifying the number of trips that are estimated to take place between each origin and each destination." also known as forecasting traffic -> estimating users on a road at one time Angelelli, E., Arsik, I., Morandi, V., Savelsbergh, M. and Speranza, M.G. (2016). Proactive route guidance to avoid congestion. Transportation Research Part B: Methodological, [online] 94, pp.1–21. doi:https://doi.org/10.1016/j.trb.2016.08.015.
‌ 

we need to manage the reaction to rush hour or holidays where the total number of users will be increased. this usually means the algorithm may be able to redirect them onto a lesser known route that will eventually save time in the process "The time period of interest is the rush hour, which in large cities may last a few hours, and in which, as Sheffi (1985) points out, traffic often exhibits a steady-state behavior"

Possible metrics to consider:
 -Travel Time, -Congestion Score (user based), -Route recalculation frequency, computational runtime for the algorithm and path optimality (we dont want a user to go back on themselves for hours to end up being in the same spot they started.)

As stated in [Measuring Traffic Congestion] it states that "The distribution of traffic is evaluated by two measures: the minimum maximum arc utilization in the network (a system perspective) and the weighted average experienced travel inconvenience (a user perspective). Arc utilization, i.e., the ratio of the number of vehicles entering an arc per time unit and its capacity,". Which would allow us to keep a track of the number of vehicles on a specific road and then update weight scores depending on the total (Capacity of the road / number of vehicles on the road can give us a total weight score that will effect the algorithms decisions. )

issue arised when trying to add a large volume of vehicles with the error message: "Traceback (most recent call last):
  File "/Users/harvey/PycharmProjects/Neural-Traffic-Routing-and-Congestion-Optimisation-System/src/graph.py", line 121, in <module>
    runSimulation()
  File "/Users/harvey/PycharmProjects/Neural-Traffic-Routing-and-Congestion-Optimisation-System/src/graph.py", line 57, in runSimulation
    vehicle = Vehicle(
  File "/Users/harvey/PycharmProjects/Neural-Traffic-Routing-and-Congestion-Optimisation-System/src/vehicle.py", line 17, in __init__
    self.route = nx.shortest_path(
  File "/Users/harvey/PycharmProjects/Neural-Traffic-Routing-and-Congestion-Optimisation-System/.venv/lib/python3.9/site-packages/networkx/utils/backends.py", line 412, in __call__
    return self.orig_func(*args, **kwargs)
  File "/Users/harvey/PycharmProjects/Neural-Traffic-Routing-and-Congestion-Optimisation-System/.venv/lib/python3.9/site-packages/networkx/algorithms/shortest_paths/generic.py", line 175, in shortest_path
    _, paths = nx.bidirectional_dijkstra(G, source, target, weight)
  File "/Users/harvey/PycharmProjects/Neural-Traffic-Routing-and-Congestion-Optimisation-System/.venv/lib/python3.9/site-packages/networkx/utils/backends.py", line 412, in __call__
    return self.orig_func(*args, **kwargs)
  File "/Users/harvey/PycharmProjects/Neural-Traffic-Routing-and-Congestion-Optimisation-System/.venv/lib/python3.9/site-packages/networkx/algorithms/shortest_paths/weighted.py", line 2431, in bidirectional_dijkstra
    raise nx.NetworkXNoPath(f"No path between {source} and {target}.")
networkx.exception.NetworkXNoPath: No path between 27480442 and 1411621893.
 "

Find how many vehicles are on each type of road

traffic by road type " Traffic Volumes by Road Type (GB)A-Roads (44% of Traffic): The highest volume, with approximately 149.7 billion vehicle miles as of September 2025. These are arterial routes.Minor Roads (35% of Traffic): Includes B-roads, C-roads, and unclassified roads, with roughly 117.5 billion vehicle miles. These are local distributor roads and residential streets.Motorways (21% of Traffic): Around 70.6 billion vehicle miles, representing high-volume, high-speed regional travel."

EXACT FIGURES COMPUTABLE : Motorways: Average of ~21,000 vehicles/day.A Roads: Average of ~16,000 vehicles/day.B Roads: Average of ~11,000 vehicles/day.Minor Roads: Average of ~5,000 vehicles/day
Xmap.ai. (2024). The United Kingdom Road Traffic in 2024: Everything You need to know. [online] Available at: https://www.xmap.ai/blog/the-united-kingdom-road-traffic-in-2024-everything-you-need-to-know.
‌

Implementation of A* -> useful benchmark as an informed search with a direct upgrade to the original Dijkstras algorithm already used.
uses heuristics to estimate costs from the start to goal-> if nodes are too far away from the goal then the alogorithm will recalulate : Sandberg, O. (2024). Pathfinding Algorithm Comparison In Dynamic Congested Environment. [online] Available at: https://www.diva-portal.org/smash/get/diva2:1879887/FULLTEXT01.pdf.
‌
Diagonal movement is allowed with euclidean distances. Combination of G-Scores and H-Scores and a pathfinding queue.

Mathematical component of A* f(n)=g(n)+h(n) Where:

* g(n) = current path cost,
* h(n) = estimated remaining cost.