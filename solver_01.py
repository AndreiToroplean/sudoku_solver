def solver(grid):
    size = grid.size ** 3

    # Building the possibilities grid:
    nb_completed = 0
    possibilities_grid = []
    for index in range(size):
        if grid.is_completed(index):
            possibilities_grid.append(None)
            nb_completed += 1
            continue
        possibilities_grid.append(grid.accepted_numbers.copy())
    initial_nb_completed = nb_completed

    # Filling the grid until complete or stuck:
    while nb_completed < size:
        previous_nb_completed = nb_completed
        for index, possibilities in enumerate(possibilities_grid):
            if possibilities is None:
                continue

            new_possibilities = []
            for proposition in possibilities:
                if grid.is_valid(index, proposition):
                    new_possibilities.append(proposition)

            if len(new_possibilities) == 1:
                grid.set_nb(index, new_possibilities[0])
                possibilities_grid[index] = None
                nb_completed += 1
                continue

            possibilities_grid[index] = new_possibilities

        if previous_nb_completed == nb_completed:
            print("Got stuck.", nb_completed - initial_nb_completed)
            print(possibilities_grid)
            break
