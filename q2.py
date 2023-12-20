"""
IE 400 - Term Project
Question 2 Script

Authors:
    - Emre Karataş, Bilkent ID: 22001641, Email: emre.karatas@ug.bilkent.edu.tr
    - Aytekin İsmail, Bilkent ID: 22003988, Email: aytekin.ismail@ug.bilkent.edu.tr
    - Ece Ateş, Bilkent ID: 22002908, Email: e.ates@ug.bilkent.edu.tr
Description:
    the goal of this script is to optimize the efficiency and energy
    consumption while taking into account the limitations and capabilities of
    each train type.
"""

# importing cplex modules and other necessary packages.
from cplex.exceptions import CplexError
from cplex import Cplex
import math

# Creating a CPLEX problem
prob = Cplex()
variables = []

# Decision Variables
X = ["X{}".format(i) for i in range(1, 16)]  # Binary decision variable for electric train in nodes 1 to 15
prob.variables.add(names=X, types=['B'] * 15)

F = ["F{}".format(i) for i in ["X", "Y"]]  # Number of fueling stations in X and Y
prob.variables.add(names=F, types=['I'] * 2)

C = ["C{}".format(i) for i in ["X", "Y"]]  # Number of charging stations in X and Y
prob.variables.add(names=C, types=['I'] * 2)

Cei = ["Ce{}".format(i) for i in range(1, 16)]  # energy cost of one train 1 - 15
prob.variables.add(names=Cei, types=['I'] * 15)

cost_variables = ["Ce", "Cr"]  # Ce = total energy usage, Cr = total cost
cost_variable_types = ['I', 'I']
prob.variables.add(names=cost_variables, types=cost_variable_types)
variables = X + F + C + Cei + cost_variables

constraints = []
coefs = []
constraint_senses = []
rhs = []

# Cx >= (x7+x13+x14)/3
prob.linear_constraints.add(
    lin_expr=[[[variables.index('CX')] + [variables.index('X{}'.format(i)) for i in [7, 13, 14]],
               [1.0, -1 / 3, -1 / 3, -1 / 3]]],
    senses=['G'],
    rhs=[0.0]
)

# Cx >= (x3+x6+x9+x11+x12+x15)/3
prob.linear_constraints.add(
    lin_expr=[[[variables.index('CX')] + [variables.index('X{}'.format(i)) for i in [3, 6, 9, 11, 12, 15]],
               [1.0, -1 / 3, -1 / 3, -1 / 3, -1 / 3, -1 / 3, -1 / 3]]],
    senses=['G'],
    rhs=[0.0]
)

# Cx >= (x2)/3
prob.linear_constraints.add(
    lin_expr=[[[variables.index('CX')] + [variables.index('X{}'.format(i)) for i in [2]], [1.0, -1 / 3]]],
    senses=['G'],
    rhs=[0.0]
)

# CY >= (x8)/3
prob.linear_constraints.add(
    lin_expr=[[[variables.index('CY')] + [variables.index('X{}'.format(i)) for i in [8]], [1.0, -1 / 3]]],
    senses=['G'],
    rhs=[0.0]
)

# CY >= (x1+x4+x5+x10)/3
prob.linear_constraints.add(
    lin_expr=[[[variables.index('CY')] + [variables.index('X{}'.format(i)) for i in [1, 4, 5, 10]],
               [1.0, -1 / 3, -1 / 3, -1 / 3, -1 / 3]]],
    senses=['G'],
    rhs=[0.0]
)

# Fx >= (3-(x7+x13+x14))/2
prob.linear_constraints.add(
    lin_expr=[[[variables.index('FX')] + [variables.index('X{}'.format(i)) for i in [7, 13, 14]],
               [1.0, 1 / 2, 1 / 2, 1 / 2]]],
    senses=['G'],
    rhs=[3 / 2]
)

# Fx >= (6-(x3+x6+x9+x11+x12+x15))/2
prob.linear_constraints.add(
    lin_expr=[[[variables.index('FX')] + [variables.index('X{}'.format(i)) for i in [3, 6, 9, 11, 12, 15]],
               [1.0, 1 / 2, 1 / 2, 1 / 2, 1 / 2, 1 / 2, 1 / 2]]],
    senses=['G'],
    rhs=[3]
)

# Fx >= (1-(x2))/2
prob.linear_constraints.add(
    lin_expr=[[[variables.index('FX')] + [variables.index('X{}'.format(i)) for i in [2]], [1.0, 1 / 2]]],
    senses=['G'],
    rhs=[1 / 2]
)

# Fy >= (1-(x8))/2
prob.linear_constraints.add(
    lin_expr=[[[variables.index('FY')] + [variables.index('X{}'.format(i)) for i in [8]], [1.0, 1 / 2]]],
    senses=['G'],
    rhs=[1 / 2]
)

# Fy >= (4-(x1+x4+x5+x10))/2
prob.linear_constraints.add(
    lin_expr=[[[variables.index('FY')] + [variables.index('X{}'.format(i)) for i in [1, 4, 5, 10]],
               [1.0, 1 / 2, 1 / 2, 1 / 2, 1 / 2]]],
    senses=['G'],
    rhs=[2.0]
)
# trains' energy constraints
prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce1'), variables.index('X1')], [1.0, (20 * 80)]]],
    senses=['E'],
    rhs=[(20 * 100)]
)

# Cei = wi(xi*20$ + (1-xi)*100$), where wi is the train i's working hours parameter
prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce2'), variables.index('X2')], [1.0, (20 * 80)]]],
    senses=['E'],
    rhs=[(20 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce3'), variables.index('X3')], [1.0, (18 * 80)]]],
    senses=['E'],
    rhs=[(18 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce4'), variables.index('X4')], [1.0, (20 * 80)]]],
    senses=['E'],
    rhs=[(20 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce5'), variables.index('X5')], [1.0, (20 * 80)]]],
    senses=['E'],
    rhs=[(20 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce6'), variables.index('X6')], [1.0, (18 * 80)]]],
    senses=['E'],
    rhs=[(18 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce7'), variables.index('X7')], [1.0, (12 * 80)]]],
    senses=['E'],
    rhs=[(12 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce8'), variables.index('X8')], [1.0, (14 * 80)]]],
    senses=['E'],
    rhs=[(14 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce9'), variables.index('X9')], [1.0, (18 * 80)]]],
    senses=['E'],
    rhs=[(18 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce10'), variables.index('X10')], [1.0, (20 * 80)]]],
    senses=['E'],
    rhs=[(20 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce11'), variables.index('X11')], [1.0, (18 * 80)]]],
    senses=['E'],
    rhs=[(18 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce12'), variables.index('X12')], [1.0, (18 * 80)]]],
    senses=['E'],
    rhs=[(18 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce13'), variables.index('X13')], [1.0, (12 * 80)]]],
    senses=['E'],
    rhs=[(12 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce14'), variables.index('X14')], [1.0, (12 * 80)]]],
    senses=['E'],
    rhs=[(12 * 100)]
)

prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce15'), variables.index('X15')], [1.0, (18 * 80)]]],
    senses=['E'],
    rhs=[(18 * 100)]
)

# Ce = Ce1 + … + Ce15
prob.linear_constraints.add(
    lin_expr=[[[variables.index('Ce{}'.format(i)) for i in range(1, 16)] + [variables.index('Ce')],
               [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0]]],
    senses=['E'],
    rhs=[0.0]
)

# Cr = (15-sum(xi))*250$ + sum(xi)*750$ + (Cx+Cy)*1,000$ + (Fx+Fy)*800$ + (C1 + … + C15)*350$ (the last part couldn't
# have been implemented in cplex code)
prob.linear_constraints.add(
    lin_expr=[[[variables.index('Cr')] + [variables.index('X{}'.format(i)) for i in range(1, 16)] + [
        variables.index('CX')] + [variables.index('CY')] + [variables.index('FX')] + [variables.index('FY')],
               [-1.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0,
                500.0, 1000.0, 1000.0, 800.0, 800.0]]],
    senses=['E'],
    rhs=[-3750.0]
)

# objective function
objective_coef = [1.0, 1.0]
objective_var = ['Ce', 'Cr']
prob.objective.set_sense(prob.objective.sense.minimize)

# solve the problem
prob.objective.set_linear(list(zip(objective_var, objective_coef)))
prob.solve()
initial_solution = prob.solution.get_values()
initial_objective_value = prob.solution.get_objective_value()

print("Variable:", variables)
print("Solution:", initial_solution)
print("Objective Value:", initial_objective_value)

# End of q2.py
