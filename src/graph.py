import networkx as nx
import matplotlib as mpl
import osmnx as os
from geopy.geocoders import Nominatim

#create the weighted graph using the library networkx.

#obtain closest node from the given area.

#obtain user inputs
loc = Nominatim(user_agent="GetLoc") #calling the Nominatim tool to get location

#location of start location
userLocationStart = input("Enter Start Location: ")
get_loc = loc.geocode(userLocationStart)
#obtain latitude and longitude coordinates from get_loc
lon1 = get_loc.longitude
lat1 = get_loc.latitude


l1 = (lat1,lon1)

G = os.graph_from_point(l1, network_type='drive', dist=500)
l1_node_id = os.nearest_nodes(G, lon1, lat1) #obtain closes node from locational points

#location of goal location
userLocationGoal = input("Enter Start Location: ")
get_loc = loc.geocode(userLocationGoal)
#obtain latitude and longitude coordinates from get_loc
lon2 = get_loc.longitude
lat2 = get_loc.latitude

l2 = (lat2,lon2)
#obtain roads/intersections/nodes
G = os.graph_from_point(l2, network_type='drive', dist=500)
l2_node_io = os.nearest_nodes(G, lat2, lon2) #obtain nearest goal node location

#calculate distance between the start and goal
dist = os.distance.great_circle(lat1,lon1,lat2,lon2)

print(f"Distance from Start to Goal is {dist} metres")

#visually display output
os.plot_graph(G)




