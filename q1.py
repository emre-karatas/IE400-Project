"""
IE 400 - Term Project
Question 1 Script

Authors:
    - Emre Karataş, Bilkent ID: 22001641, Email: emre.karatas@ug.bilkent.edu.tr
    - Aytekin İsmail, Bilkent ID: 22003988, Email: aytekin.ismail@ug.bilkent.edu.tr
    - Ece Ateş, Bilkent ID: 22002908, Email: e.ates@ug.bilkent.edu.tr
Description:
    This python script aims to solve assigning the trains to the 2 fixed depots (X and Y) by
    minimizing the distance traveled by trains.
"""

# importing cplex modules.
from cplex.exceptions import CplexError
from cplex import Cplex

# Creating a CPLEX problem
model = Cplex()

# Setting model objective to minimize.
model.objective.set_sense(model.objective.sense.minimize)

# Adding variables.
# Detailed expression is given in the report document.
num_variables = 15
variables = ['x{}'.format(i) for i in range(1, num_variables + 1)]
binary_variables = variables + ['y{}'.format(i) for i in range(1, num_variables + 1)]

# Adding binary integer variables
model.variables.add(names=binary_variables, types='B' * (2 * num_variables))

# Set objective coefficients to solve the problem
objective_coefficients = [2.0, 2.0, 2.0, 4.0, 6.0, 2.0, 2.0, 2.0, 2.0, 4.0, 2.0, 2.0, 2.0, 2.0, 2.0,
                          6.0, 4.0, 2.0, 2.0, 2.0, 4.0, 6.0, 4.0, 2.0, 2.0, 6.0, 6.0, 4.0, 2.0, 4.0]

model.objective.set_linear(list(zip(binary_variables, objective_coefficients)))

# Adding constraint xi + yi = 1 for all i
for i in range(1, num_variables + 1):
    indices = [variables.index('x{}'.format(i)), binary_variables.index('y{}'.format(i))]
    model.linear_constraints.add(
        lin_expr=[[indices, [1.0, 1.0]]],
        senses=['E'],
        rhs=[1.0]
    )

# Adding constraints for the sums - 1
model.linear_constraints.add(
    lin_expr=[[[variables.index('x{}'.format(i)) for i in [1, 7, 11, 12]], [1.0, 1.0, 1.0, 1.0]]],
    senses=['L'],
    rhs=[3.0]
)

# Adding constraints for the sums - 2
model.linear_constraints.add(
    lin_expr=[[[binary_variables.index('y{}'.format(i)) for i in [1, 7, 11, 12]], [1.0, 1.0, 1.0, 1.0]]],
    senses=['L'],
    rhs=[3.0]
)

# Adding constraints for the sums - 3
model.linear_constraints.add(
    lin_expr=[[[variables.index('x{}'.format(i)) for i in [2, 8, 13, 15]], [1.0, 1.0, 1.0, 1.0]]],
    senses=['L'],
    rhs=[3.0]
)

# Adding constraints for the sums - 4
model.linear_constraints.add(
    lin_expr=[[[binary_variables.index('y{}'.format(i)) for i in [2, 8, 13, 15]], [1.0, 1.0, 1.0, 1.0]]],
    senses=['L'],
    rhs=[3.0]
)

# Adding constraints for the sums of all xis and yis
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

print(binary_variables)


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

# End of q1.py
