from routing.simulation import (
    run_simulation
)


def main():
    """
    Main simulation entry point.
    """

    num_vehicles = int(
        input(
            "Enter number of vehicles: "
        )
    )

    algorithm = input(
        "Choose algorithm "
        "(dijkstra/astar): "
    ).strip().lower()

    if algorithm not in [
        "dijkstra",
        "astar"
    ]:

        raise ValueError(
            "Invalid routing algorithm."
        )

    run_simulation(

        num_vehicles=num_vehicles,

        algorithm=algorithm,

        use_neural_network=False

    )


if __name__ == "__main__":

    main()