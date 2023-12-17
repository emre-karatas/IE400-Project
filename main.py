import cplex
from cplex.exceptions import CplexError
from cplex import Cplex

# Create a CPLEX problem
model = Cplex()


model.objective.set_sense(model.objective.sense.minimize)
# Add variables
num_variables = 15
variables = ['x{}'.format(i) for i in range(1, num_variables + 1)]
binary_variables = variables + ['y{}'.format(i) for i in range(1, num_variables + 1)]

# Add binary integer variables
model.variables.add(names=binary_variables, types='B' * (2 * num_variables))

# Set objective function (if needed)
objective_coefficients = [1.0,3.0,1.0,2.0,1.0,1.0,2.0,1.0,3.0,1.0,1.0,2.0,1.0,3.0,1.0,2.0,1.0,1.0,2.0,1.0,1.0,3.0,1.0,3.0,1.0,2.0,1.0,1.0,1.0,2.0]
model.objective.set_linear(list(zip(binary_variables, objective_coefficients)))

# Add constraint xi + yi = 1 for all i
for i in range(1, num_variables + 1):
    indices = [variables.index('x{}'.format(i)), binary_variables.index('y{}'.format(i))]
    model.linear_constraints.add(
        lin_expr=[[indices, [1.0, 1.0]]],
        senses=['E'],
        rhs=[1.0]
    )

# Add constraints for the sums
model.linear_constraints.add(
    lin_expr=[[[variables.index('x{}'.format(i)) for i in [1, 7, 11, 12]], [1.0, 1.0, 1.0, 1.0]]],
    senses=['L'],
    rhs=[3.0]
)

model.linear_constraints.add(
    lin_expr=[[[binary_variables.index('y{}'.format(i)) for i in [1, 7, 11, 12]], [1.0, 1.0, 1.0, 1.0]]],
    senses=['L'],
    rhs=[3.0]
)

model.linear_constraints.add(
    lin_expr=[[[variables.index('x{}'.format(i)) for i in [2, 8, 13, 15]], [1.0, 1.0, 1.0, 1.0]]],
    senses=['L'],
    rhs=[3.0]
)

model.linear_constraints.add(
    lin_expr=[[[binary_variables.index('y{}'.format(i)) for i in [2, 8, 13, 15]], [1.0, 1.0, 1.0, 1.0]]],
    senses=['L'],
    rhs=[3.0]
)

# Add constraints for the sums of all xis and yis
model.linear_constraints.add(
    lin_expr=[[[variables.index('x{}'.format(i)) for i in range(1, num_variables + 1)], [1.0] * num_variables]],
    senses=['G'],
    rhs=[5.0]
)

model.linear_constraints.add(
    lin_expr=[[[binary_variables.index('y{}'.format(i)) for i in range(1, num_variables + 1)], [1.0] * num_variables]],
    senses=['G'],
    rhs=[5.0]
)

# Solve the problem
try:
    model.solve()
    print("Solution status:", model.solution.get_status())
    print("Objective value:", model.solution.get_objective_value())
    print("Solution:")
    for i, val in enumerate(model.solution.get_values()):
        print(f"{model.variables.get_names(i)}: {val}")

except CplexError as exc:
    print(exc)
