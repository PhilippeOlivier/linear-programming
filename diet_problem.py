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
v_names = ["x_1", "x_2", "x_3", "x_4", "x_5", "x_6"]

# We must buy at least 0 of each type of food.
v_lower_bounds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# We impose a servings-per-day limit on all foods so as not to become sick.
v_upper_bounds = [4.0, 3.0, 2.0, 8.0, 2.0, 2.0]

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
c_names = ["c_1", "c_2", "c_3"]

c1_lhs_coefficients = [110.0, 205.0, 160.0, 160.0, 420.0, 260.0]
c2_lhs_coefficients = [4.0, 32.0, 13.0, 8.0, 4.0, 14.0]
c3_lhs_coefficients = [2.0, 12.0, 54.0, 285.0, 22.0, 80.0]

c_rhs = [2000.0, 55.0, 800.0]
c_senses = ["G", "G", "G"]

problem.linear_constraints.add(lin_expr = [[v_names, c1_lhs_coefficients],
                                           [v_names, c2_lhs_coefficients],
                                           [v_names, c3_lhs_coefficients]],
                               senses = c_senses,
                               rhs = c_rhs,
                               names = c_names)

# Supress CPLEX output
problem.set_error_stream(None)
problem.set_log_stream(None)
problem.set_results_stream(None)
problem.set_warning_stream(None)

# Solve the problem.
problem.solve()

print("=== MODEL "+"="*70)
print("""
min   3x_1 +  24x_2 +  13x_3 +   9x_4 +  20x_5 +  19x_6
s.t.
    110x_1 + 205x_2 + 160x_3 + 160x_4 + 420x_5 + 260x_6 >= 2000    (c_1)
      4x_1 +  32x_2 +  13x_3 +   8x_4 +   4x_5 +  14x_6 >=   55    (c_2)
      2x_1 +  12x_2 +  54x_3 + 285x_4 +  22x_5 +  80x_6 >=  800    (c_3)
       x_1                                              <=    4
                x_2                                     <=    3
                         x_3                            <=    2
                                  x_4                   <=    8
                                           x_5          <=    2
                                                    x_6 <=    2
       x_1                                              >=    0
                x_2                                     >=    0
                         x_3                            >=    0
                                  x_4                   >=    0
                                           x_5          >=    0
                                                    x_6 >=    0
""", end='')

food_names = ["oatmeal",
              "chicken",
              "eggs",
              "whole milk",
              "cherry pie",
              "pork with beans"]

print("\n=== SOLUTION "+"="*67)
print("Objective value:", problem.solution.get_objective_value())
for i in range(problem.variables.get_num()):
    print("Buy ", problem.solution.get_values(i), " of ", v_names[i],
          " (", food_names[i], ")", sep='')

print("\n=== DUAL VALUES "+"="*64)
for i in range(problem.linear_constraints.get_num()):
    print(c_names[i], "dual value:", problem.solution.get_dual_values(i))

print("""
A dual value (also called dual price, or shadow price) is associated with each
constraint of the primal problem. This value represents the improvement in the
objective function if the right-hand side of the constraint were relaxed by one
unit. In our case, c_1 has a dual value of 0.05625, meaning that by relaxing the
right-hand side of c_1 by one unit (since 2000 is a lower limit, relaxing it by
one unit means bringing it to 1999) the objective should improve (i.e.,
decrease, since we are minimizing) by 0.05625. Let's try it:
""")

print("Objective value before:", problem.solution.get_objective_value(), "\n")
print("110x_1 + 205x_2 + 160x_3 + 160x_4 + 420x_5 + 260x_6 >= 1999    (c_1)\n")
problem.linear_constraints.set_rhs("c_1", 1999.0)
problem.solve()
print("Objective value after:", problem.solution.get_objective_value())

print("""
c_2 and c_3 have dual values of 0, so relaxing the right-hand side of the
constraint by one unit has no effect:
""")

print("Objective value before:", problem.solution.get_objective_value(), "\n")
print("4x_1 + 32x_2 + 13x_3 +   8x_4 +  4x_5 + 14x_6 >=  54    (c_2)")
print("2x_1 + 12x_2 + 54x_3 + 285x_4 + 22x_5 + 80x_6 >= 799    (c_3)\n")
problem.linear_constraints.set_rhs("c_2", 54.0)
problem.linear_constraints.set_rhs("c_3", 799.0)
problem.solve()
print("Objective value after:", problem.solution.get_objective_value())

print("""
Let's restore the original values for our constraints before moving to the next
section:

110x_1 + 205x_2 + 160x_3 + 160x_4 + 420x_5 + 260x_6 >= 2000    (c_1)
  4x_1 +  32x_2 +  13x_3 +   8x_4 +   4x_5 +  14x_6 >=   55    (c_2)
  2x_1 +  12x_2 +  54x_3 + 285x_4 +  22x_5 +  80x_6 >=  800    (c_3)
""")
problem.linear_constraints.set_rhs("c_1", 2000.0)
problem.linear_constraints.set_rhs("c_2", 55.0)
problem.linear_constraints.set_rhs("c_3", 800.0)
problem.solve()

print("=== REDUCED COSTS "+"="*62)
for i in range(problem.variables.get_num()):
    print(v_names[i], "reduced cost:", problem.solution.get_reduced_costs(i))

print("""
A reduced cost (also called opportunity cost) is associated with each variable
of the primal problem. This value represents the amount by which the coefficient
of the associated variable in the objective function would have to improve
(i.e., decrease, since we are minimizing) before it would be profitable for this
variable to assume a nonzero value. Thus, variables which have a value of zero
in the objective function have a positive reduced cost, and variables which have
a nonzero value have a zero reduced cost.

Let's take x_3 for example: Its value in the solution is 0, its coefficient in
the objective function is 13, and its reduced cost is 4. This means that if the
coefficient of x_3 improves by more than its reduced cost (i.e., decreases,
since we are minimizing) in the objective function, then it should be profitable
to give some value to x_3 in the solution. The reduced cost of x_3 is 4, so
let's improve his coefficient in the objective function by 5 and see what
happens:
""")

print("Objective value before:", problem.solution.get_objective_value())
print("x_3 value in the solution before:", problem.solution.get_values(2))
print("x_3 coefficient in the objective function before: 13")
print("x_3 reduced cost before:", problem.solution.get_reduced_costs(2))
problem.objective.set_linear("x_3", 8.0)
problem.solve()
print("\nObjective value after:", problem.solution.get_objective_value())
print("x_3 value in the solution after:", problem.solution.get_values(2))
print("x_3 coefficient in the objective function after: 8")
print("x_3 reduced cost after:", problem.solution.get_reduced_costs(2))
