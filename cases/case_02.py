from z3 import *

def check_utilitarian_proportionality():
    # Crime Severity (1 = Shoplifting, 5 = Threat to Life)
    C_sev = Int('C_sev') 
    T = Real('T')        # Face-match threshold
    R = Int('R')         # Candidate return limit
    SearchPermitted = Bool('SearchPermitted')
    
    s = Solver()
    s.add(And(C_sev >= 1, C_sev <= 5))
    s.add(R >= 1)
    
    # Utilitarian Rules for Proportionality
    # Rule 1: Low severity requires strict threshold (>= 0.9)
    rule_low_sev = Implies(C_sev == 1, And(T >= 0.9, R == 1))
    # Rule 2: High severity permits relaxed threshold (>= 0.8) to maximize catch rate
    rule_high_sev = Implies(C_sev == 5, And(T >= 0.8, R <= 20))
    
    s.add(rule_low_sev, rule_high_sev)
    
    # Test Scenario: Operator investigates a severe crime (C_sev = 5) 
    # and sets T = 0.80 to cast a wider net.
    s.add(C_sev == 5)
    s.add(T == 0.80)
    s.add(R == 10)
    s.add(SearchPermitted == True)
    
    if s.check() == sat:
        print("Utilitarian Check PASSED: T=0.80 is proportional for C_sev=5.")
    else:
        print("Utilitarian Check FAILED: T=0.80 is NOT proportional for C_sev=5.")

if __name__ == "__main__":
    check_utilitarian_proportionality()