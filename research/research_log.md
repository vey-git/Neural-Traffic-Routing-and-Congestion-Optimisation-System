research notes:

background thesis-> many people dislike congestion as it is an irritant causing their personal schedules to be out of their control, it is a financial loss in some cases where people may not be able to make it to work and the cost of fuel, especially in this economy for standstill traffic. --> traffic congestion means that there are more vehicles trying to use a given road than it can handle without exceeding levels of delay or inconvenience. Occurs certain times of the day in major cites and this is called "peak periods" or "rush hours"


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

Neural networks -> Basic neuron structure = left weights, determine right neuron, the higher the weight the higher the activation. Right most neuron is the output of the network,

Types of models: Hopfield model is an additive model where the individual weights of the neurons are totaled to find the activation of the final neuron. Uses a fully interconnected network of neuron to descend onto an energy function. $E = -\frac{1}{2}\sum_{i,j} w_{ij} x_i x_j + \sum_i \theta_i x_i$ : T ( i , j )are the interconnection weights,I ( i )are the input biases,U(i)are the internal states,V(i)are the neuron outputs, andg(x)is a nonlinear activation function which can be taken asg(x)=-1+tanh-[13

Gilmore, J. F. and Abe, N. (1995) ‘NEURAL NETWORK MODELS FOR TRAFFIC CONTROL AND CONGESTION PREDICTION’, I V H S Journal, 2(3), pp. 231–252. doi: 10.1080/10248079508903828.
https://www.tandfonline.com/doi/abs/10.1080/10248079508903828?casa_token=k1WuWLrjCo0AAAAA:f9TTeB7kdwYhbkiNxnqxcv8_V2tCR4ghdGcoWAtOsFiFxxghODuzvKzFbws6esaKIZ8THRjv

The reason this model would be good for this project, is we would be able to total the number of congested roads compared to our current location, and also total the number of cars within a certain viscinity which could alter the path our newly formed neural network parses to our vehicles.
Asynchronised update rule is implemented which periodically changes a randoms neurons weight until it matches the result we are looking for, in this case: less congested roads/pathways

Hopfield networks are attractive for congestion optimisation due to its energy restriction behaviour, which conceptually aligns with reducing the total network congestion. However, their recurrent fully-connected structure may scale poorly for large urban traffic systems and could be less suitable for supervised travel-time regression compared to the later model explained in this research log
Arulampalam, G. and Bouzerdoum, A. (2003). A generalized feedforward neural network architecture for classification and regression. Neural Networks, 16(5-6), pp.561–568. doi:https://doi.org/10.1016/s0893-6080(03)00116-3.
‌

Feedforward neural network model:

used by a non-linear differential equation by shunting a portion of the signal. Shunting inhibition: reducing the number of operations/neurons passed while maintaining efficacy

each neuron used by the differential equation is described by the following:

$\frac{dx_j}{dt} = I_j - a_j x_j - f \sum_i c_{ji} x_i x_j + b_j$

where xj represents the activity of the current neuron, Ij is the input of the jth neuron. aj is the passive decay rate of the neuron. cji is the connection weight from the ith input to the jth neuron. bj represents the bias and f is an activation function.

in a feedforward model, both the excitatory and inhibitory influences are mediated by the external inputs.
 xi term in the previous equation is replaced by Ij 

$\frac{dx_j}{dt} = I_j - a_j x_j - f \sum_i c_{ji} I_i x_j + b_j$

the static shunting neruon is derived from the steady-state solution of the previous equation. the state of the static shunting neuron is given by:

$x_j = I_j + b_j a_j + f \sum_i c_{ji} I_i + c_{jo}$

The number of neurons in a network is dependant on the size of the dataset. The number of neurons in the shunting layer(s) is determined by the number of data attributes, whereas the number of neurons in the output layer is determined by the number of class labels. This is by using the basic SIAAN structure. Downside is that it is too restrictive although removed the need to find an optimal network structure.

Generalised shunting neuron model:

this has excitatory inputs summed and passed through an activation function with a perceptron neuron. G. Arulampalam, A. Bouzerdoum
Expanding the structure of shunting inhibitory artificial neural network classifiers
Proceedings of the International Joint Conference on Neural Networks (IJCNN 2002), Honolulu, USA (2002), pp. 2855-2860

This new model combines perceptron neuron model with the shunting neuron model as described earlier. The output can be described as:

$x_j = g \sum_i w_{ji} I_i + w_{j0} + b_j a_j + f \sum_i c_{ji} I_i + c_{j0}$
where wjj=1 and all other weights wji are 0, g is the linear activation function. The perceptron model is a special case of the GSN, where the demoninator weights c are fixed at 0 and a is set to a constant in order to make the denominator equal to 1 depending on the activation function.

Reasons the feedforward implementation is the best for our neutral network:

feasible from scratch

fits within our trained data appropriately, taking use of all fields

supports supervised learning

integrates naturally with routing metrics

Types of evaluations

Chicco, D., Warrens, M.J. and Jurman, G. (2021). The Coefficient of Determination R-squared Is More Informative than SMAPE, MAE, MAPE, MSE and RMSE in Regression Analysis Evaluation. PeerJ Computer Science, [online] 7(5), p.e623. doi:https://doi.org/10.7717/peerj-cs.623.
‌

MSE = best value is 0, can be used if there are outliers that need to be detected, if the model finds a significant outlier, then the square function highlights this accordingly. this is important for our metrics as we are able to determine what sort of routes are causing issues, and where most traffic is being funneled towards
 
n
1
​	
 ∑ 
i=1
n
​	
 (Y 
i
​	
 − 
Y
^
  
i
​	
 ) 
2

What is a ANN? computations of a brain are done by a highly interconnected network of neurons, which communicate by sending electric pulses through the neural wiring which consists of axons, synapses and dendrites : Krogh, A. What are artificial neural networks?. Nat Biotechnol 26, 195–197 (2008). https://doi.org/10.1038/nbt1386
they can be created by simulating a network of model neurons in a computer. Applying algorihtms that mimic the processes of real neurons we can make a network "learn" to solve many types of problems. A neuron is referred to as a threshold unit and recieves an input from a number of other units or external sources, weighs each input and then sums them. If the total input is above a threshold then the output of a unit is a 1 else a 0