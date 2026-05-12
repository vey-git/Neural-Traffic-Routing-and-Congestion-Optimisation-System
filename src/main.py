from simulation import runSimulation


num_of_vehicles = int(
    input("How many vehicles do you want to simulate?: ")

)
algorithm = "astar"


runSimulation(num_of_vehicles, algorithm)