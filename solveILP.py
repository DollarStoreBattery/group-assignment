# SYDE 411, 2021
# The Branch and Bound Solution for Integer Linear Programming
# Group 22

from scipy.optimize import linprog
import math

class SolveILP(object):
    def __init__(self, fn_coeffs, constraint_coeffs, constraints, bounds, isMaximization = True):
        # these do not change even when branching out
        self.fn_coeffs = fn_coeffs
        self.bounds = bounds
        self.isMaximization = isMaximization
        self.result = {}

        return self.solve_ILP(constraints,constraint_coeffs)

    def evaluate_objective_function(self,design_vector):
        f = 0
        # it's a linear function so it's just a sum of c_n * x_n
        for index, x in enumerate(design_vector):
            f += self.fn_coeffs[index] * x
        return f
            
    def get_LP_relaxed(self,constraints,constraint_coeffs):
        # linprog always returns the minimum of a function
        c = self.fn_coeffs
        if self.isMaximization:
            # multiply all values by negative -1 to switch to a maximization
            c = [i * -1 for i in self.fn_coeffs]       
        return linprog(c=c, bounds=self.bounds, A_ub=constraint_coeffs,b_ub=constraints,method='revised simplex')

    def find_branching_variable(self,design_vector):
        # need to select the design variable with the highest number after the first decimal point
        decimal_vals = list(map(lambda x: x % 1, design_vector))
        idx = decimal_vals.index(max(decimal_vals))
        return (design_vector[idx], idx)

    def get_upper_bound(self,relaxed_solution,design_vector):
        if self.isMaximization:
            upper_bound = relaxed_solution
            # round down in maximization
            # rounded_variables = list(map(lambda x: math.floor(x), design_vector))
            # lower_bound = self.evaluate_objective_function(rounded_variables)
        else:
            # lower_bound = relaxed_solution
            # round up in minimization
            rounded_variables = list(map(lambda x: math.ceil(x), design_vector))
            upper_bound = self.evaluate_objective_function(rounded_variables)
        return upper_bound

    def solve_ILP(self,constraints,constraint_coeffs):
        # Get LP-relaxed Solution
        relaxed_solution = self.get_LP_relaxed(constraints,constraint_coeffs)

        design_variables = relaxed_solution.x 
        function_value = -1 * relaxed_solution.fun if self.isMaximization else relaxed_solution.fun

        # print("Design Variables: ", design_variables)
        # print("Function Value: ",function_value )

        # Check if we can stop, by seeing if all the values are integers 
        all_are_integers = all(x - int(x) == 0 for x in design_variables)

        if all_are_integers:
            # A solution has been found!
            self.result = {"x":design_variables, "f": function_value}
            return 

        else:
            # Determine which design variable to branch off of
            branching_variable, idx = self.find_branching_variable(design_variables)
            # print("branching variable: ", branching_variable)
            # Branch the variable into two new constraints

            # left branch: value rounded down
            left_branch= math.floor(branching_variable)
            # right branch: value rounded up
            right_branch = math.ceil(branching_variable)

            # print("left branch. must be less than: ", left_branch)
            # print("right_branch. must be greather than: ",right_branch)
            # Set up a new constraint array, applying the constraint only the design variable of index
            new_constraint_array = [0]*len(design_variables)
            new_constraint_array[idx] = 1
            
            # add to constraints that the design variable must be lte the left branch value
            left_constraints = constraints + [left_branch]
            left_constraints_coeffs  = constraint_coeffs + [new_constraint_array]

            # add to constraints that the design variable must be gte the right branch value
            # since linprog always evaluates inequalities with LTE, use negative value to flip inequality 
            right_constraints = constraints + [-1*right_branch]
            flipped_constraints = [i * -1 for i in new_constraint_array] 
            right_constraints_coeffs = constraint_coeffs + [flipped_constraints]

            # Get the LP_relaxed solutions for the left and right branches
            left_optimization = self.get_LP_relaxed(left_constraints, left_constraints_coeffs)
            right_optimization = self.get_LP_relaxed(right_constraints,right_constraints_coeffs)

            # change function value accordingly if we are doing maximization
            left_val = -1 * left_optimization.fun if self.isMaximization else left_optimization.fun
            right_val = -1 * right_optimization.fun if self.isMaximization else right_optimization.fun

            left_ub = self.get_upper_bound(left_val,left_optimization.x) if left_optimization.success else None
            right_ub = self.get_upper_bound(right_val,right_optimization.x) if right_optimization.success else None

            # print("left upper bound: ", left_ub)
            # print("right upper bound: ", right_ub)

            # the recursive act of branching left or right
            def move_left():
                # print("Moving Left")
                self.solve_ILP(left_constraints, left_constraints_coeffs)
            def move_right():
                # print("Moving Right")
                self.solve_ILP(right_constraints,right_constraints_coeffs)


            # based off the LP relaxation,
            # decide where to branch off depending on which upper bound is higher and also whether it was feasible
            # the .success flag tells you if it was feasible

            if left_optimization.success and right_optimization.success:
                # if left_val > right_val:
                if left_ub > right_ub:
                    move_left()
                else:
                    move_right()
            elif left_optimization.success:
                    move_left()
            elif right_optimization.success:
                    move_right()
            else:
                self.result = {"x":None, "f": None}
                return