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
