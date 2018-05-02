### THE DIET PROBLEM ###########################################################
#
# The values for this example, as well as the description of the problem, are
# taken from pages 3-5 of "Linear programming, by Vasek Chvatal, W. H. Freeman
# and Company, New York, 1983".
#
# The diet problem is described as follows:
#
# Polly wonders how much money she must spend on food in order to get all the
# energy (2,000 kcal), protein (55 g), and calcium (800 mg) that she needs every
# day.
#
# |-----------------+--------+---------+---------+-------------------|
# |                 | Energy | Protein | Calcium | Price per serving |
# |-----------------+--------+---------+---------+-------------------|
# | Oatmeal         |    110 |       4 |       2 |                 3 |
# | Chicken         |    205 |      32 |      12 |                24 |
# | Eggs            |    160 |      13 |      54 |                13 |
# | Whole milk      |    160 |       8 |     285 |                 9 |
# | Cherry pie      |    420 |       4 |      22 |                20 |
# | Pork with beans |    260 |      14 |      80 |                19 |
# |-----------------+--------+---------+---------+-------------------|
#
# She decides to impose servings-per-day limits on all six foods:
#
# |-----------------+----------------------------|
# | Oatmeal         | at most 4 servings per day |
# | Chicken         | at most 3 servings per day |
# | Eggs            | at most 2 servings per day |
# | Whole milk      | at most 8 servings per day |
# | Cherry pie      | at most 2 servings per day |
# | Pork with beans | at most 2 servings per day |
# |-----------------+----------------------------|
#
################################################################################


import cplex


# We initialize the problem.
problem = cplex.Cplex()

# We set the objective for minimization since we want to minimize the amount of
# money that must spend on food.
problem.objective.set_sense(problem.objective.sense.minimize)

# Decision variables: How much of each type of food will we buy?
v_names = ["oatmeal",
           "chicken",
           "eggs",
           "whole milk",
           "cherry pie",
           "pork with beans"]

# We must buy at least 0 of each type of food.
v_lower_bounds = [0.0,
                  0.0,
                  0.0,
                  0.0,
                  0.0,
                  0.0]

# We impose a servings-per-day limit on all foods so as not to become sick.
v_upper_bounds = [4.0,
                  3.0,
                  2.0,
                  8.0,
                  2.0,
                  2.0]

# The price per serving is represented by the coefficients of the decision
# variables in the objective function.
v_objective_coefficients = [3.0, 24.0, 13.0, 9.0, 20.0, 19.0]

# We add the variables to the problem.
problem.variables.add(obj = v_objective_coefficients,
                      lb = v_lower_bounds,
                      ub = v_upper_bounds,
                      names = v_names)

# The additional constraints are to meet the requirements for energy, protein,
# and calcium.
c_names = ["c1",
           "c2",
           "c3"]

c1_lhs_coefficients = [110.0, 205.0, 160.0, 160.0, 420.0, 260.0]
c2_lhs_coefficients = [4.0, 32.0, 13.0, 8.0, 4.0, 14.0]
c3_lhs_coefficients = [2.0, 12.0, 54.0, 285.0, 22.0, 80.0]

c_rhs = [2000.0,
         55.0,
         800.0]
c_senses = ["G",
            "G",
            "G"]

problem.linear_constraints.add(lin_expr = [[v_names, c1_lhs_coefficients],
                                           [v_names, c2_lhs_coefficients],
                                           [v_names, c3_lhs_coefficients]],
                               senses = c_senses,
                               rhs = c_rhs,
                               names = c_names)

# Solve the problem.
problem.solve()
solution = problem.solution.get_values(0, problem.variables.get_num()-1)

# Print the solution.
print("="*80)
print("="*80)
print("Objective value:", problem.solution.get_objective_value())
for i in range(problem.variables.get_num()):
    print("Buy", solution[i], "of", v_names[i])
