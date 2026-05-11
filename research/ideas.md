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