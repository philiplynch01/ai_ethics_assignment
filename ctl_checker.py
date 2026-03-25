from z3 import *

# Recall from our class discussions, that Z3 is not a native CTL checker. 
#  Z3 is primarily an SMT solver (dealing with satisfiability). To solve CTL problems, 
# we perform Symbolic Model Checking. We use Z3 to represent sets of states as Boolean 
# formulas and implement the CTL fixpoint algorithms (like AF, EG) using Python loops.

class SymbolicModelChecker:
    def __init__(self):
        self.s = Solver()
    
    # 1. Define the Transition Relation T(curr, next)
    def set_model(self, variables, trans_relation, init_condition):
        self.vars = variables  # List of Z3 Bool variables (current state)
        # Create primed variables for next state (e.g., x -> x_prime)
        self.primed_vars = [Bool(str(v) + "_prime") for v in self.vars]
        self.trans = trans_relation
        self.init = init_condition
        
        # Helper: Map current vars to primed vars in a formula
        self.to_prime = [(self.vars[i], self.primed_vars[i]) for i in range(len(self.vars))]

    # 2. Basic Helpers
    def get_primed(self, formula):
        return substitute(formula, self.to_prime)

    # 3. CTL Operators (Symbolic Implementation)
    
    # EX(phi): There exists a next state where phi is true
    # Logic: exists(next_vars). (T(curr, next) AND phi(next))
    def EX(self, phi):
        phi_prime = self.get_primed(phi)
        f = Exists(self.primed_vars, And(self.trans, phi_prime))
        # Use quantifier elimination (tactic) to simplify
        t = Tactic('qe')
        return t(f).as_expr()

    # AX(phi) = NOT EX (NOT phi)
    def AX(self, phi):
        return Not(self.EX(Not(phi)))

    # AF(phi): In All paths, Future phi (Liveness)
    # Fixpoint: X = phi OR AX(X)
    def AF(self, phi):
        X = BoolVal(False) 
        while True:
            X_new = simplify(Or(phi, self.AX(X)))
            if X_new.eq(X): return X 
            X = X_new

    # EF(phi): Exists Future phi (Reachability)
    # Fixpoint: X = phi OR EX(X)
    def EF(self, phi):
        X = BoolVal(False)
        while True:
            X_new = simplify(Or(phi, self.EX(X)))
            if X_new.eq(X): return X
            X = X_new

    # AG(phi): Always Global phi (Safety)
    # Logic: NOT EF (NOT phi)
    def AG(self, phi):
        return Not(self.EF(Not(phi)))

    # EG(phi): Exists Global phi (Infinite path)
    # Fixpoint: X = phi AND EX(X)
    def EG(self, phi):
        X = BoolVal(True)
        while True:
            X_new = simplify(And(phi, self.EX(X)))
            if X_new.eq(X): return X
            X = X_new

    # 4. Verify
    def check(self, ctl_formula):
        # Check if Initial State implies the formula
        # If Init => Formula is valid, then NOT(Init => Formula) is UNSAT
        self.s.reset()
        self.s.add(Not(Implies(self.init, ctl_formula)))
        if self.s.check() == unsat:
            print(f"Property Verified: {ctl_formula}")
            return True
        else:
            print(f"Counter-example found for: {ctl_formula}")
            # print(self.s.model()) # Optional: print the state that failed
            return False