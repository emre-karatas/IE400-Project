import cplex

# values of the file depot_node_distances.txt
x_to_stations = [1, 1, 1, 2, 3, 2, 1, 1]
y_to_stations = [3, 2, 1, 1, 1, 1, 1, 2]

# values of the file distances.txt
distances = [
    [0, 1, 2, 1, 1, 2, 2, 1],
    [1, 0, 1, 1, 2, 3, 1, 3],
    [2, 1, 0, 1, 2, 2, 3, 2],
    [1, 1, 1, 0, 1, 2, 1, 2],
    [1, 2, 2, 1, 0, 1, 3, 2],
    [2, 3, 2, 2, 1, 0, 1, 2],
    [2, 1, 3, 1, 3, 1, 0, 1],
    [1, 3, 2, 2, 2, 2, 1, 0]
]

# paths from the file paths.txt
paths = [
    ['A', 'C', 'H', 'B'],
    ['B', 'G', 'A'],
    ['C', 'G', 'D'],
    ['D', 'F', 'E', 'G', 'C'],
    ['E', 'F', 'C'],
    ['H', 'G', 'F'],
    ['A', 'H', 'G', 'E'],
    ['B', 'H', 'C'],
    ['C', 'E', 'H'],
    ['F', 'G', 'E', 'A', 'B', 'C', 'D', 'E'],
    ['A', 'B', 'C'],
    ['A', 'F'],
    ['B', 'F', 'D'],
    ['G', 'C', 'E'],
    ['B', 'D', 'G']
]

# This dictionary helps convert the station name into its index
# Usage example: distance from station A to station F = distances[station['A'], station['F']]
station_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
# Initialize CPLEX problem
problem = cplex.Cplex()
problem.objective.set_sense(problem.objective.sense.minimize)

# Create binary decision variables for each train for depots X and Y
x_vars = [f"x_{i+1}" for i in range(15)]
y_vars = [f"y_{i+1}" for i in range(15)]
problem.variables.add(names=x_vars + y_vars, types=["B"] * 30)

# Define the objective function
objective = []
for i, path in enumerate(paths):
    start_station = station_index[path[0]]
    end_station = station_index[path[-1]]
    distance_to_x = x_to_stations[start_station]
    distance_to_y = y_to_stations[start_station]
    objective.append((x_vars[i], 2 * distance_to_x))
    objective.append((y_vars[i], 2 * distance_to_y))

problem.objective.set_linear(objective)

# Constraints
# Each train assigned to exactly one depot
for i in range(15):
    problem.linear_constraints.add(
        lin_expr=[[[x_vars[i], y_vars[i]], [1, 1]]],
        senses=["E"],
        rhs=[1]
    )

# Each depot has at least 5 trains
problem.linear_constraints.add(
    lin_expr=[[x_vars, [1] * 15]],
    senses=["G"],
    rhs=[5]
)
problem.linear_constraints.add(
    lin_expr=[[y_vars, [1] * 15]],
    senses=["G"],
    rhs=[5]
)

# Solve the problem
try:
    problem.solve()
except cplex.CplexError as e:
    print("Cplex Error:", e)
    exit()

# Print the solution
for var in x_vars + y_vars:
    print(f"{var}: {problem.solution.get_values(var)}")

# Print the objective value
print("Objective value:", problem.solution.get_objective_value())