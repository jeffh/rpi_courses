#from constraint import Problem # I don't like GPL code!

class Constraint(object):
    def __init__(self, func, variables):
        self._func, self._vars = func, variables
        
    def __call__(self, *args, **kwargs):
        if len(args) + len(kwargs) < len(self._vars):
            raise TypeError, "Constraint Function requires %r arguments" % len(self._vars)
        return self._func(*args, **kwargs)
    
    def __len__(self):
        return len(self._vars)
        
    def __cmp__(self, other):
        return cmp(len(self), len(other))

class SolverTree(object):
    def __init__(self, variables, constraints):
        self._vars, self._constraints = variables, []
        for func, variables in constraints:
            self._constraints.append(Constraint(func, variables))
        self._constraints.sort()
        self._constraints.reverse()
    
    def __iter__(self):
        variables_size = {}

# public API
class Problem(object):
    def __init__(self, solver_class=SolverTree):
        self._solver_class
        self._variables = {} # variable: domain
        self._constraints = [] # (constraint_function, variables)
    
    def add_variable(self, variable, domain):
        self._variables[variable] = domain
    
    def add_constraint(self, func, variables):
        self._constraints.append((func, variables))
    
    def get_solutions(self):
        result = []
        solver = self._solver_class(self._variables, self._constraints)
        for answer in solver:
            result.append(answer)
        return result