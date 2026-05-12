Task is to generate the following: a system that is able to display roads, intersections, traffic and movement.
This can be done by a weighted graph. 

Node1 ---5---> Node2 // where nodes represent intersections, weighted using a value.

Initially had it where the goal and start node was imputed by a string, however this was approximate location which could effect the total result. To change this alter the start and goal to take coordinates of the user.

First action is to create the strongest classical implementation for routing: in this case Dijkstra algorithm 

The map was initially very hard to understand as the colours merged, this was fixed by changing red to a cian and giving it an appropriate title for clarity.

now all the routing is working as it should we need to implement a road cost for traffic conditions, when multiple vehicles are added then that road will be congested leading to a longer journey through that route. initially we will use static values so get the algorithm working first.

Next stage -> create a vehicle for simulation on roads. Each vehicle has a start and goal node, we then randomise the location based on the main geographical area we want to focus on, in this case it is OXFORD. So we could geenrate multiple vehicles at a time to simulate real congestion on roads. we want to be able to pick a location from the nodes on the current graph, not random coordinates as some of these coordinates will not be roads.

changed hard-coded locational values, using random variable nodes on the master graph to create vehicles for simulation: fixed by using Try and Except -> to get the following algorithm flow for each vehicle:

    valid_route = False

    while not valid_route:

        generate random nodes

        try:
            create vehicle

            add vehicle

            valid_route = True

        except:
            retry

Now that this is working we are able to give each rode a capacity. This will be researched -> Motorways will most likely have the highst capacity compared to residential areas. Check //research_log.md// to find this.

To calculate this we want to increment the traffic count every time an edge appears on that given road 

Next case is we could find the average of all edges within the graph. if an edge is more than average its travel_time is increased if its less then its decreased : 
< 0.5

Very low traffic

1.0x

0.5 – 1.0

Normal traffic

1.1x

1.0 – 1.5

Moderate congestion

1.4x

1.5 – 2.0

Heavy congestion

1.8x

2.0

Severe congestion

2.5x

we have an average, if the edge/road is less than the average it stays at the baseline speed as it wont speed up the route

Visual update
:implement a heatmap for roads 

With the newly updated congestion weighting we would expect the vehicles to take alternate paths if they pass through a heavily weighted edge. In theory there should be more green lanes compared to reds vs the first vehicle routing path.

To test whether our vehicles are updating based on the weights, i am going to comment out the code for rerouting, run the program with 25 vehicles initially and then stress test on 250. then add the rerouting code back and run the same amount of vehicles and see if the graph has any changes
From first run without rerouting: "some red congestion with a fair few yellow congestions but still mainly green".
2nd run: issue with implementation, the computational power needed grew exponentially, and i needed to end the program as it was not efficient.
Issue: recalculating the route for every vehicle each time it loops which meant for a huge overhead in computational power
Fix: calculate all vehicles, then reroute them all.

Updated: First run on 25 vehicles: completed almost instantaneously with a few yellow routes but no red.

2nd run on 250 vehicles (non rerouting): completed quickly, some red and yellow congestion

3rd run with rerouting (25 vehicles): 1 or 2 yellow pathways

4th run with rerouting (250 vehicles): not expected but there is more congestion in certain areas, more red and yellow 

Found an issue "edge = (route[1], route[i+1])" where route[1] should be route[i] which creates a bottleneck

Secondary issue is the loop is still in the wrong area, i moved it but not far enough out of the loop

Changes in code to fix all these issues: moved congestion logic outside of the vehicle "for loop", added a base_travel_time as previous weight calculation exploded exponentially which could provide instability when calculating reroutes, rerouting now only happens once.

Test1: Run without reroute on 250 vehicles: ran instantaneous, huge pathways of red and yellow congestion, means the weighting was the issue. average edge usage is 4.379789631855748

Test2: Run with reroute on 250 vehicles: similar congestion with a score of: 4.379789631855748

both edge usage for with and without reroute are similar, which makes me think there is a bug. 
issue is that the output is still on the non rerouting vehicles, the plot stays the same and doesnt update, meaning the reroute does occur however we can visually see the change. Fix: update the plot and reset edge usage and update with the new edge usage 

Test to see if the routes are the same with and without rerouting on 5 vehicles:
Routes are the exact same with and without the routing so there is an issue "                 #debug for routes
                print(f"Route: {vehicle.route}")" this was the debug. Going to try and alter the multiplier on weights

Added debugging outputs which allowed me to see the code works with a change of "for key in edge_data:" instead of first_key = list(edge_data.keys())[0] when recalculating using the Digraph

Retesting with 250 vehicles: out of 250, 51 of them changed their routes with an average edge usage of 5.095901313171508
25: Vehicles with changed routes: 5

Average Edge Usage AFTER: 1.4023809523809523
50: Vehicles with changed routes: 9

Average Edge Usage AFTER: 1.8960720130932898
100:Vehicles with changed routes: 15

Average Edge Usage AFTER: 3.187732342007435

There is still congestion as these weights wont completely negate congestion, the vehicles are only determining what the shortest path from their current node is, in theory many of the vehicles will have the same shortest path, we can see this in the figure where most congestion comes from routes that have no alternatives, for example a long highway.

This highlights that obtaining the shortest path for each vehicle is insufficient as a singular algorithm to mitigate congestion
