from solveILP import SolveILP
from google_or import solve_CBC
from time import perf_counter
# This is the machine shop example from http://web.tecnico.ulisboa.pt/mcasquilho/compute/_linpro/TaylorB_module_c.pdf
# Maximize Z = 100*(x_1) + 150(x_2)
# Subject to:
# 8000*(x_1) + 4000*(x_2) <= 40,000
# 15*(x_1) + 30*(x_2) <= 200
# x1,x2 >= zero 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Coefficients for Z (objective function equation)
c = [100, 150]

# Coeffecients of the Constraints 
# 2D Array => each entry is a constraint, each element within the entry are the coefficients for the design variable within the constraint
A = [[8000, 4000], [15, 30]]

# The other side of the inequalitiy (must be in less than or equal to format) for each constraint
b = [40000, 200]

# The range of values, None representing infinity 
bounds = [(0,None),(0,None)]

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
