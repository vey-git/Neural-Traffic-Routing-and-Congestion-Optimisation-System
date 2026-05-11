Task is to generate the following: a system that is able to display roads, intersections, traffic and movement.
This can be done by a weighted graph. 

Node1 ---5---> Node2 // where nodes represent intersections, weighted using a value.

Initially had it where the goal and start node was imputed by a string, however this was approximate location which could effect the total result. To change this alter the start and goal to take coordinates of the user.

First action is to create the strongest classical implementation for routing: in this case Dijkstra algorithm 
