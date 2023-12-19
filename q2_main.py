from cplex import Cplex
from cplex.exceptions import CplexError

# Create a new Cplex object
model = Cplex()

# Decision variables
# Xi: 1 if the train is electric, 0 if diesel
xi = [f"x{i}" for i in range(1, 16)]
model.variables.add(names=xi, types=["B"] * 15)  # Binary variables

# Costs
ce = "ce"  # Cost of energy
cr = "cr"  # Other costs
model.variables.add(names=[ce, cr], types=["C", "C"])  # Continuous variables

# Number of charging and fueling stations
cx = "cx"
cy = "cy"
fx = "fx"
fy = "fy"
ci = [f"c{i}" for i in range(1, 16)]
model.variables.add(names=[cx, cy, fx, fy] + ci, types=["I"] * (4 + 15))  # Integer variables

# Objective function: Minimize Ce + Cr
model.objective.set_sense(model.objective.sense.minimize)
model.objective.set_linear([(ce, 1), (cr, 1)])

# Assuming Dij (distance between nodes) and Ti (cycling count) are given as parameters
# Example data (Replace with actual data)
Dij = [[...], [...], ...]  # Replace with actual distances
Ti = [...]  # Replace with actual cycling counts

# Constraints
# Energy cost for each train
for i in range(1, 16):
    train_var = xi[i - 1]
    energy_cost_electric = 16 * 20000 * Ti[i - 1]  # Example calculation for electric
    energy_cost_diesel = 16 * 100000 * Ti[i - 1]   # Example calculation for diesel
    model.linear_constraints.add(
        lin_expr=[[train_var], [1]],
        senses=["E"],
        rhs=[energy_cost_electric + (1 - energy_cost_electric) * energy_cost_diesel]
    )

# Total energy cost
model.linear_constraints.add(
    lin_expr=[[xi, ["1"] * 15], [ce, -1]],
    senses=["E"],
    rhs=[0]
)

# Other costs
model.linear_constraints.add(
    lin_expr=[[xi, ["-1"] * 15], [cx, 1], [cy, 1], [fx, 1], [fy, 1], [ci, ["1"] * 15], [cr, -1]],
    senses=["E"],
    rhs=[15 * 250000 - 750000 - 1000000 - 800000 - 350000]
)

# Solve the model
try:
    model.solve()
except CplexError as exc:
    print(exc)
    return

# Print the solution
print("Solution status =", model.solution.get_status())
print("Solution value  =", model.solution.get_objective_value())

# Print the values of decision variables
for var in xi + [ce, cr, cx, cy, fx, fy] + ci:
    print(f"{var} =", model.solution.get_values(var))
