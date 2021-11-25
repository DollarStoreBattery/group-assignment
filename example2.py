from solveILP import SolveILP
from google_or import solve_CBC
from time import perf_counter


# Maximize Z = 5x1 + 3x2 + 7y1 + 2y2
# Subject to:
# 7x1 + 8x2 + 9y1 +3y2 <=43
# 11x1 + 4x2 + 4y1 + 5y2 <= 51
# x1,x2,y1,y2 >= zero 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Coefficients for Z (objective function equation)
c = [5,3,7,2]

# Coeffecients of the Constraints 
# 2D Array => each entry is a constraint, each element within the entry are the coefficients for the design variable within the constraint
A = [[7,8,9,2], [11,4,4,5]]

# The other side of the inequalitiy (must be in less than or equal to format) for each constraint
b = [43, 51]

# The range of values, None representing infinity 
bounds = [(0,None),(0,None),(0,None),(0,None)]

start_time = perf_counter()
our_soln = SolveILP(c,A,b, bounds)
end_time = perf_counter()

print("branch and bound: ", our_soln.result)
print("branch and bound time (ms): ", format((end_time - start_time)*1000,'.2f'))

data = {
    'constraint_coeffs': A,
    'bounds': b,
    'obj_coeffs': c,
    'num_vars': len(c),
    'num_constraints': len(A)
}

rival_soln = solve_CBC(data)
 