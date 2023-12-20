import cplex
import numpy as np

# Read the input data
paths = np.loadtxt("paths.txt", delimiter=" ")
parameters = np.loadtxt("parameters.txt", delimiter=" ")

# Define the decision variables
x = cplex.VarArray(shape=(15, 15), name="x")  # Train assignments to paths
y = cplex.VarArray(shape=(2, 15), name="y")  # Depot assignments to trains
z = cplex.VarArray(shape=(10, 2), name="z")  # Charging/fueling station assignments to nodes

# Define the objective function
objective = cplex.Objective(expr=cplex.sum(parameters[0, x.flat] * x.flat) +
                                cplex.sum(parameters[1, y.flat] * y.flat) +
                                cplex.sum(parameters[2, z.flat] * z.flat))

# Add the constraints
model = cplex.Cplex()
model.add(objective)

# Each train must be assigned to exactly one path
for i in range(15):
    model.add(cplex.Eq(cplex.sum(x[i, :]), 1))

# Each path must be assigned to at least one train
for j in range(15):
    model.add(cplex.Ge(cplex.sum(x[:, j]), 1))

# Each train must be assigned to a depot
for i in range(15):
    model.add(cplex.Eq(cplex.sum(y[:, i]), 1))

# Each depot must have at most 3 electric trains and 2 diesel trains assigned to it
for j in range(2):
    model.add(cplex.Le(cplex.sum(y[j, :]), parameters[3, j]))

# Each node must have at most 1 charging/fueling station
for i in range(10):
    model.add(cplex.Le(cplex.sum(z[i, :]), 1))

# Each electric train must be charged at least once every 8 hours
for i in range(15):
    for j in range(15):
        if paths[j, 1] - paths[j, 0] > 8:
            model.add(cplex.Le(cplex.sum(z[paths[j, 0], 0] * x[i, j]), 1))

# Each diesel train must be refueled at least once every 20 hours
for i in range(15):
    for j in range(15):
        if paths[j, 1] - paths[j, 0] > 20:
            model.add(cplex.Le(cplex.sum(z[paths[j, 0], 1] * x[i, j]), 1))

# Solve the model
model.solve()

# Print the results
print("Train assignments to paths:")
print(x.get_values())

print("Depot assignments to trains:")
print(y.get_values())

print("Charging/fueling station assignments to nodes:")
print(z.get_values())

print("Total cost:", model.solution.get_objective_value())