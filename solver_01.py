def _calc_completion(possibilities_len, row_len):
    return (row_len - possibilities_len) / ((row_len - 1) * possibilities_len)


def solver(grid):
    numbers_len = len(grid.numbers)

    # Building the possibilities grid:
    completion = 0.0
    possibilities_grid = []
    for index in range(numbers_len):
        if grid.is_completed(index):
            possibilities_grid.append(None)
            completion += 1
            continue
        possibilities_grid.append(grid.accepted_numbers.copy())
    initial_completion = completion

    iterations = 0
    guesses = 0
    backtracks = 0

    # Filling the grid until complete or stuck:
    while completion < numbers_len:
        previous_completion = completion
        for index, possibilities in enumerate(possibilities_grid):
            if possibilities is None:
                continue

            checked_possibilities = []
            for proposition in possibilities:
                if grid.is_valid(index, proposition):
                    checked_possibilities.append(proposition)

            completion += (_calc_completion(len(checked_possibilities), grid.row_len)
                           - _calc_completion(len(possibilities), grid.row_len))

            if len(checked_possibilities) == 1:
                grid.set_nb(index, checked_possibilities[0])
                possibilities_grid[index] = None
                continue

            possibilities_grid[index] = checked_possibilities

        iterations += 1

        if previous_completion == completion:
            break

    print(f"Took it from {initial_completion*100/numbers_len:.1f}% "
          f"to {completion*100/numbers_len:.1f}% completed over {iterations} iterations.")
